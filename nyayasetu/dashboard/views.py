from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from complaints.models import Complaint
from departments.models import Department
import json

def get_global_stats():
    """Helper to get global complaint statistics."""
    total_complaints = Complaint.objects.count()
    total_resolved = Complaint.objects.filter(status='resolved').count()
    total_pending = Complaint.objects.filter(status='pending').count()
    total_escalated = Complaint.objects.filter(status='escalated').count()
    total_administrative_failures = Complaint.objects.filter(status='administrative_failure').count()
    
    return {
        'total_complaints': total_complaints,
        'total_resolved': total_resolved,
        'total_pending': total_pending,
        'total_escalated': total_escalated,
        'total_administrative_failures': total_administrative_failures,
    }

def get_department_stats():
    """Helper to get detailed department statistics."""
    return Department.objects.annotate(
        total_complaints=Count('complaints', filter=Q(complaints__is_deleted=False)),
        resolved_count=Count('complaints', filter=Q(complaints__status='resolved', complaints__is_deleted=False)),
        failure_count=Count('complaints', filter=Q(complaints__status='administrative_failure', complaints__is_deleted=False))
    ).order_by('-transparency_score')

@login_required
def citizen_dashboard(request):
    # Redirect officers/staff to their dashboard
    if request.user.role != 'citizen':
        return redirect('officer_dashboard')
        
    user_complaints = Complaint.objects.filter(created_by=request.user)
    
    # User Specific Stats
    user_total_complaints = user_complaints.count()
    user_resolved = user_complaints.filter(status='resolved').count()
    user_pending = user_complaints.filter(status='pending').count()
    user_escalated = user_complaints.filter(status='escalated').count()
    user_admin_failure = user_complaints.filter(status='administrative_failure').count()
    
    from django.utils import timezone
    user_overdue = user_complaints.filter(
        sla_deadline__lt=timezone.now()
    ).exclude(status__in=['resolved', 'administrative_failure']).count()
    
    status_counts = user_complaints.values('status').annotate(count=Count('status'))
    
    # Global & Department Stats
    global_stats = get_global_stats()
    departments = get_department_stats()
    
    context = {
        'user_total_complaints': user_total_complaints,
        'user_resolved': user_resolved,
        'user_pending': user_pending,
        'user_escalated': user_escalated,
        'user_admin_failure': user_admin_failure,
        'user_overdue': user_overdue,
        'status_counts': status_counts,
        'departments': departments,
        **global_stats,  # Unpack global stats into context
    }
    return render(request, 'dashboard/citizen_dashboard.html', context)

@login_required
def officer_dashboard(request):
    if request.user.role == 'citizen':
        return redirect('citizen_dashboard')
        
    # Officer Specific Stats
    assigned_complaints = Complaint.objects.filter(assigned_to=request.user)
    assigned_count = assigned_complaints.count()
    
    # Check overdue (approximate check against now)
    from django.utils import timezone
    now = timezone.now()
    overdue_count = assigned_complaints.filter(
        sla_deadline__lt=now
    ).exclude(status__in=['resolved', 'administrative_failure']).count()
    
    escalated_count = Complaint.objects.filter(
        assigned_to=request.user, 
        status='escalated'
    ).count()
    
    officer_resolved_count = Complaint.objects.filter(
        assigned_to=request.user,
        status='resolved'
    ).count()
    
    # Get recent complaints for display
    recent_complaints = assigned_complaints.order_by('-sla_deadline')[:10]
    
    # Global & Department Stats
    global_stats = get_global_stats()
    departments = get_department_stats()
    
    geolocated_complaints = Complaint.objects.filter(
        department=request.user.department,
        latitude__isnull=False,
        longitude__isnull=False
    ).values('id', 'title', 'urgency_level', 'status', 'latitude', 'longitude', 'city', 'state')
    
    map_complaints_list = []
    for c in geolocated_complaints:
        map_complaints_list.append({
            'id': c['id'],
            'title': c['title'],
            'urgency_level': c['urgency_level'],
            'status': c['status'],
            'latitude': float(c['latitude']),
            'longitude': float(c['longitude']),
            'city': c['city'] or '',
            'state': c['state'] or ''
        })

    context = {
        'assigned_count': assigned_count,
        'overdue_count': overdue_count,
        'escalated_count': escalated_count,
        'officer_resolved_count': officer_resolved_count,
        'department': request.user.department,
        'recent_complaints': recent_complaints,
        'now': now,
        'departments': departments,
        'map_complaints_json': json.dumps(map_complaints_list),
        **global_stats, # Unpack global stats into context
    }
    return render(request, 'dashboard/officer_dashboard.html', context)

def get_location_stats():
    """Helper to get complaint statistics by State and City."""
    state_stats = Complaint.objects.values('state').annotate(total=Count('id')).order_by('-total')
    city_stats = Complaint.objects.values('city').annotate(total=Count('id')).order_by('-total')[:10]  # Top 10 cities
    return {
        'state_stats': state_stats,
        'city_stats': city_stats
    }

def public_dashboard(request):
    # Global & Department Stats
    global_stats = get_global_stats()
    departments = get_department_stats()
    location_stats = get_location_stats()
    
    # Prepare JSON data for charts
    # Pie Chart Data: Status Distribution
    status_data = {
        'labels': ['Resolved', 'Pending', 'Escalated', 'Admin Failure'],
        'data': [
            global_stats['total_resolved'], 
            global_stats['total_pending'], 
            global_stats['total_escalated'], 
            global_stats['total_administrative_failures']
        ],
        'backgroundColor': ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
    }
    
    # Bar Chart Data: Transparency Scores and Failures
    dept_names = [dept.name for dept in departments]
    transparency_scores = [dept.transparency_score for dept in departments]
    failure_counts = [dept.failure_count for dept in departments]
    
    bar_data = {
        'labels': dept_names,
        'transparency': transparency_scores,
        'failures': failure_counts
    }

    # Location Data for Charts (Optional, can be added to template later)
    state_labels = [item['state'] for item in location_stats['state_stats'] if item['state']]
    state_data = [item['total'] for item in location_stats['state_stats'] if item['state']]
    
    location_chart_data = {
        'labels': state_labels,
        'data': state_data
    }
    
    geolocated_complaints = Complaint.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).values('id', 'title', 'urgency_level', 'status', 'latitude', 'longitude', 'city', 'state')
    
    map_complaints_list = []
    for c in geolocated_complaints:
        map_complaints_list.append({
            'id': c['id'],
            'title': c['title'],
            'urgency_level': c['urgency_level'],
            'status': c['status'],
            'latitude': float(c['latitude']),
            'longitude': float(c['longitude']),
            'city': c['city'] or '',
            'state': c['state'] or ''
        })

    context = {
        'departments': departments,
        'status_json': json.dumps(status_data),
        'bar_json': json.dumps(bar_data),
        'location_json': json.dumps(location_chart_data),
        'map_complaints_json': json.dumps(map_complaints_list),
        **global_stats, # Unpack global stats into context
        **location_stats, # Unpack location stats into context
    }
    return render(request, 'dashboard/public_dashboard.html', context)
