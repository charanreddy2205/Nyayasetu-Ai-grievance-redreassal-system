from typing import Any
from django.db.models import Count, Q
from django.utils import timezone
from django.core.cache import cache
from complaints.models import Complaint
from departments.models import Department
from api.constants import (
    STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_RESOLVED, STATUS_ESCALATED, 
    STATUS_ADMINISTRATIVE_FAILURE, ROLE_CITIZEN
)

class DashboardService:
    """
    Service layer providing dashboard stats calculations and map pinning data mapping.
    """
    
    @staticmethod
    def get_public_stats_data() -> dict:
        """
        Calculates public statistical distributions and active map marker pins.
        Uses Redis caching for high availability and low latency.
        """
        CACHE_KEY = 'public_dashboard_stats'
        cached_stats = cache.get(CACHE_KEY)
        if cached_stats:
            return cached_stats

        # Optimize global metrics counts in one query using database aggregations
        stats = Complaint.objects.aggregate(
            total=Count('id'),
            resolved=Count('id', filter=Q(status=STATUS_RESOLVED)),
            pending=Count('id', filter=Q(status=STATUS_PENDING)),
            escalated=Count('id', filter=Q(status=STATUS_ESCALATED)),
            failures=Count('id', filter=Q(status=STATUS_ADMINISTRATIVE_FAILURE))
        )
        total_complaints = stats['total']
        total_resolved = stats['resolved']
        total_pending = stats['pending']
        total_escalated = stats['escalated']
        total_failures = stats['failures']

        # Optimize department joins
        departments = Department.objects.annotate(
            total_complaints=Count('complaints'),
            resolved_count=Count('complaints', filter=Q(complaints__status=STATUS_RESOLVED)),
            failure_count=Count('complaints', filter=Q(complaints__status=STATUS_ADMINISTRATIVE_FAILURE))
        ).order_by('-transparency_score')

        dept_data = []
        for d in departments:
            dept_data.append({
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "totalComplaints": d.total_complaints,
                "resolvedCount": d.resolved_count,
                "failureCount": d.failure_count,
                "transparencyScore": d.transparency_score
            })

        # Aggregation of states
        state_stats = Complaint.objects.values('state').annotate(total=Count('id')).order_by('-total')
        state_data = [{"state": s['state'] or "Unknown", "total": s['total']} for s in state_stats if s['state']]

        # Top 10 cities
        city_stats = Complaint.objects.values('city').annotate(total=Count('id')).order_by('-total')[:10]
        city_data = [{"city": c['city'] or "Unknown", "total": c['total']} for c in city_stats]

        # Geolocated pins for leaflet map visualization
        geolocated = Complaint.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).values('id', 'title', 'urgency_level', 'status', 'latitude', 'longitude', 'city', 'state')

        map_data = []
        for g in geolocated:
            map_data.append({
                "id": g['id'],
                "title": g['title'],
                "urgency": g['urgency_level'],
                "status": g['status'],
                "latitude": float(g['latitude']),
                "longitude": float(g['longitude']),
                "city": g['city'] or "",
                "state": g['state'] or ""
            })

        result = {
            "total": total_complaints,
            "resolved": total_resolved,
            "pending": total_pending,
            "escalated": total_escalated,
            "failures": total_failures,
            "departments": dept_data,
            "states": state_data,
            "cities": city_data,
            "mapPins": map_data
        }
        
        # Cache for 5 minutes
        cache.set(CACHE_KEY, result, 300)
        return result

    @staticmethod
    def get_dashboard_stats(user: Any) -> dict:
        """
        Aggregates dashboard stats injected with user-role metadata.
        """
        stats = DashboardService.get_public_stats_data()
        now = timezone.now()

        if user.is_authenticated:
            if user.role == ROLE_CITIZEN:
                user_complaints = Complaint.objects.filter(created_by=user)
                user_stats = user_complaints.aggregate(
                    total=Count('id'),
                    resolved=Count('id', filter=Q(status=STATUS_RESOLVED)),
                    pending=Count('id', filter=Q(status=STATUS_PENDING)),
                    escalated=Count('id', filter=Q(status=STATUS_ESCALATED)),
                    overdue=Count('id', filter=Q(sla_deadline__lt=now) & ~Q(status__in=[STATUS_RESOLVED, STATUS_ADMINISTRATIVE_FAILURE]))
                )
                stats["user"] = {
                    "role": ROLE_CITIZEN,
                    "total": user_stats['total'],
                    "resolved": user_stats['resolved'],
                    "pending": user_stats['pending'],
                    "escalated": user_stats['escalated'],
                    "overdue": user_stats['overdue']
                }
            else:
                assigned_complaints = Complaint.objects.filter(current_owner=user)
                officer_stats = assigned_complaints.aggregate(
                    assigned=Count('id'),
                    resolved=Count('id', filter=Q(status=STATUS_RESOLVED)),
                    escalated=Count('id', filter=Q(status=STATUS_ESCALATED)),
                    overdue=Count('id', filter=Q(sla_deadline__lt=now) & ~Q(status__in=[STATUS_RESOLVED, STATUS_ADMINISTRATIVE_FAILURE]))
                )
                
                dept_geolocated = Complaint.objects.filter(
                    department=user.department,
                    latitude__isnull=False,
                    longitude__isnull=False
                ).values('id', 'title', 'urgency_level', 'status', 'latitude', 'longitude', 'city', 'state') if user.department else []

                dept_map_pins = []
                for g in dept_geolocated:
                    dept_map_pins.append({
                        "id": g['id'],
                        "title": g['title'],
                        "urgency": g['urgency_level'],
                        "status": g['status'],
                        "latitude": float(g['latitude']),
                        "longitude": float(g['longitude']),
                        "city": g['city'] or "",
                        "state": g['state'] or ""
                    })

                stats["user"] = {
                    "role": "officer",
                    "assigned": officer_stats['assigned'],
                    "overdue": officer_stats['overdue'],
                    "escalated": officer_stats['escalated'],
                    "resolved": officer_stats['resolved'],
                    "departmentName": user.department.name if user.department else None,
                    "departmentMapPins": dept_map_pins
                }

        return stats
