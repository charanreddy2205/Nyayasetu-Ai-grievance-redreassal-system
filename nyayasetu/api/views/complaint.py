import logging
import urllib.request
import urllib.parse
import json
from decimal import Decimal
from django.utils import timezone
from django.http import HttpRequest
import django_filters
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from complaints.models import Complaint
from api.serializers.complaint import ComplaintSerializer, CommentSerializer, ComplaintCreateSerializer
from api.services.complaint_service import ComplaintService
from api.services.comment_service import CommentService
from api.permissions import IsComplaintParticipant
from api.exceptions import ValidationException

logger = logging.getLogger(__name__)

class OptionalPageNumberPagination(PageNumberPagination):
    """
    PageNumberPagination subclass that only paginates if the 'page' parameter is provided.
    This maintains 100% backwards compatibility for legacy clients reading complete lists.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if 'page' not in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data) -> Response:
        return Response({
            "success": True,
            "message": "Paginated complaints list retrieved.",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
            # Backward compatibility key
            "complaints": data
        })


class ComplaintFilter(django_filters.FilterSet):
    """
    Advanced query filters mapping for complaints queries.
    """
    overdue = django_filters.BooleanFilter(method='filter_overdue')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    deadline_after = django_filters.DateTimeFilter(field_name='sla_deadline', lookup_expr='gte')
    deadline_before = django_filters.DateTimeFilter(field_name='sla_deadline', lookup_expr='lte')

    class Meta:
        model = Complaint
        fields = ['status', 'department', 'urgency_level', 'city', 'state', 'assigned_to', 'created_by']

    def filter_overdue(self, queryset, name, value):
        if value:
            now = timezone.now()
            return queryset.filter(
                sla_deadline__lt=now
            ).exclude(status__in=['resolved', 'administrative_failure'])
        return queryset


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    ViewSet handling Grievance listings, creations, details, comment updates, and status updates.
    """
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated, IsComplaintParticipant]
    pagination_class = OptionalPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ComplaintFilter
    search_fields = ['title', 'description', 'created_by__username', 'department__name']
    ordering_fields = ['created_at', 'sla_deadline', 'urgency_level', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        base_query = Complaint.objects.select_related('department', 'assigned_to', 'created_by')
        print("DEBUG get_queryset USER:", user, "ROLE:", getattr(user, 'role', 'No Role'))
        if user.role == 'citizen':
            qs = base_query.filter(created_by=user)
            print("DEBUG SQL:", str(qs.query))
            return qs
        elif user.role == 'state_admin':
            return base_query.all()
        else:
            if user.department:
                return base_query.filter(department=user.department)
            return base_query.none()

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Complaints list retrieved.",
            "data": {
                "complaints": serializer.data
            },
            "complaints": serializer.data
        })

    def create(self, request, *args, **kwargs) -> Response:
        serializer = ComplaintCreateSerializer(data=request.data)
        if serializer.is_valid():
            complaint = ComplaintService.create_complaint(
                user=request.user,
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                contact_number=serializer.validated_data.get("contact_number"),
                address=serializer.validated_data.get("address"),
                city=serializer.validated_data.get("city"),
                state=serializer.validated_data.get("state"),
                pincode=serializer.validated_data.get("pincode"),
                latitude=serializer.validated_data.get("latitude"),
                longitude=serializer.validated_data.get("longitude"),
                department_id=serializer.validated_data.get("department").id if serializer.validated_data.get("department") else None,
                image=request.FILES.get("image")
            )
            read_serializer = ComplaintSerializer(instance=complaint)
            return Response({
                "success": True,
                "message": "Complaint created successfully.",
                "data": read_serializer.data,
                "complaints": [read_serializer.data],
                "id": complaint.id,
                "title": complaint.title,
                "department": complaint.department.name if complaint.department else None,
                "urgency": complaint.urgency_level,
                "summary": complaint.summary
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "success": False,
            "message": "Validation failed.",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs) -> Response:
        complaint, comments, logs = ComplaintService.get_complaint_details(
            request.user, int(kwargs['pk'])
        )
        complaint_serializer = ComplaintSerializer(instance=complaint)
        comment_serializer = CommentSerializer(instance=comments, many=True)
        
        log_data = []
        for log in logs:
            log_data.append({
                "id": log.id,
                "escalatedTo": log.escalated_to.username if log.escalated_to else None,
                "reason": log.reason,
                "createdAt": log.created_at.isoformat()
            })
            
        data = complaint_serializer.data
        data["comments"] = comment_serializer.data
        data["logs"] = log_data
        
        return Response({
            "success": True,
            "message": "Grievance details retrieved.",
            "data": data
        })

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.delete()
        return Response({
            "success": True,
            "message": "Grievance archived successfully."
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], url_path='comments', permission_classes=[permissions.IsAuthenticated])
    def post_comment(self, request: HttpRequest, pk: str = None) -> Response:
        complaint = self.get_object()
        comment_text = request.data.get("comment_text")
        image = request.FILES.get("image")
        
        comment = CommentService.add_comment(
            user=request.user,
            complaint_id=complaint.id,
            comment_text=comment_text,
            image=image
        )
        serializer = CommentSerializer(instance=comment)
        return Response({
            "success": True,
            "message": "Comment posted successfully.",
            "data": {"comment": serializer.data},
            "comment": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST', 'PATCH'], url_path='status', permission_classes=[permissions.IsAuthenticated])
    def patch_status(self, request: HttpRequest, pk: str = None) -> Response:
        complaint = self.get_object()
        status_val = request.data.get("status")
        
        updated_complaint = ComplaintService.update_status(request.user, complaint.id, status_val)
        serializer = ComplaintSerializer(instance=updated_complaint)
        
        return Response({
            "success": True,
            "message": "Status updated successfully.",
            "data": serializer.data,
            "status": updated_complaint.status,
            "resolvedAt": updated_complaint.resolved_at.isoformat() if updated_complaint.resolved_at else None
        })


class ReverseGeocodeView(APIView):
    """
    Backend geoproxy router queries osm reverse API securely.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if not lat or not lon:
            return Response({
                "success": False,
                "message": "Latitude and longitude coordinates are required.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            float(lat)
            float(lon)
        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid coordinates formatting.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'NyayaSetu-GrievancePortal-Backend/1.0'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                return Response(data)
        except Exception as e:
            logger.error(f"Reverse geocode proxy failed: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "Reverse lookup API request failed.",
                "data": None
            }, status=status.HTTP_502_BAD_GATEWAY)
