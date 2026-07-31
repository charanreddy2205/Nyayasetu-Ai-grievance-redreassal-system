import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm
from escalation.models import EscalationLog
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()

@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            
            # Auto-route department if not specified
            if not complaint.department_id:
                from .ai_engine import classify_department
                from departments.models import Department
                dept_name = classify_department(complaint.description)
                dept = Department.objects.filter(name__iexact=dept_name).first()
                if dept:
                    complaint.department = dept
                else:
                    complaint.department = Department.objects.first()
            
            if not complaint.department_id:
                from departments.models import Department
                complaint.department = Department.objects.first()
                
            # Auto-assign to officers in department with priority order
            # Priority: staff > hod > district_officer > state_admin
            officer_roles = ['staff', 'hod', 'district_officer', 'state_admin']
            assigned = False
            
            for role in officer_roles:
                officer = User.objects.filter(
                    department=complaint.department, 
                    role=role
                ).first()
                
                if officer:
                    complaint.assigned_to = officer
                    assigned = True
                    break
            
            # If no officer found in department, assign to any officer in that department
            if not assigned:
                officer = User.objects.filter(
                    department=complaint.department
                ).exclude(role='citizen').first()
                
                if officer:
                    complaint.assigned_to = officer
            
            try:
                complaint.save()
            except Exception as e:
                logger.error(f"Error saving complaint: {e}", exc_info=True)
                messages.error(request, f"Error saving complaint: {e}")
                return render(request, 'complaints/create.html', {'form': form})
            messages.success(request, 'Complaint lodged successfully!')
            return redirect('my_complaints')
        else:
            logger.warning("Complaint form is invalid")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/create.html', {'form': form})

@login_required
def my_complaints(request):
    from django.utils import timezone
    complaints = Complaint.objects.filter(created_by=request.user)
    
    # Filter by overdue
    if request.GET.get('overdue') == 'true':
        complaints = complaints.filter(
            sla_deadline__lt=timezone.now()
        ).exclude(status__in=['resolved', 'administrative_failure'])

    # Filter by status if provided in query params
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
        
    complaints = complaints.order_by('-created_at')
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints, 'now': timezone.now()})

@login_required
def complaint_detail(request, pk):
    from django.utils import timezone
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Ensure usage access (creator, assigned staff/admin, department officer, or state admin)
    has_access = (
        complaint.created_by == request.user or
        complaint.assigned_to == request.user or
        request.user.role == 'state_admin' or
        (request.user.role != 'citizen' and request.user.department == complaint.department)
    )
    if not has_access:
        messages.error(request, 'You do not have permission to view this complaint.')
        if request.user.role == 'citizen':
            return redirect('citizen_dashboard')
        else:
            return redirect('officer_dashboard')

    from .forms import ComplaintCommentForm
    
    if request.method == 'POST':
        comment_form = ComplaintCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.complaint = complaint
            comment.author = request.user
            comment.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('complaint_detail', pk=pk)
    else:
        comment_form = ComplaintCommentForm()

    logs = EscalationLog.objects.filter(complaint=complaint).order_by('escalated_at')
    comments = complaint.comments.all().order_by('created_at')
    
    return render(request, 'complaints/detail.html', {
        'complaint': complaint,
        'logs': logs,
        'comments': comments,
        'comment_form': comment_form,
        'now': timezone.now()
    })

@login_required
def assigned_complaints(request):
    # Check if user is officer
    if request.user.role == 'citizen':
        messages.error(request, 'Access denied.')
        return redirect('citizen_dashboard')
        
    from django.utils import timezone
    now = timezone.now()
    complaints = Complaint.objects.filter(assigned_to=request.user)
    
    # Filter by overdue
    if request.GET.get('overdue') == 'true':
        complaints = complaints.filter(
            sla_deadline__lt=now
        ).exclude(status__in=['resolved', 'administrative_failure'])
        
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
        
    complaints = complaints.order_by('sla_deadline')
    return render(request, 'complaints/assigned_list.html', {'complaints': complaints, 'now': now})

@login_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permission
    if complaint.assigned_to != request.user:
        messages.error(request, 'You are not authorized to update this complaint.')
        return redirect('assigned_complaints')
    
    from .forms import ComplaintStatusForm
    from django.utils import timezone
    
    if request.method == 'POST':
        form = ComplaintStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            updated_complaint = form.save(commit=False)
            if updated_complaint.status == 'resolved':
                updated_complaint.resolved_at = timezone.now()
            updated_complaint.save()
            messages.success(request, 'Complaint status updated.')
            return redirect('assigned_complaints')
    else:
        form = ComplaintStatusForm(instance=complaint)
        
    return render(request, 'complaints/update_status.html', {'form': form, 'complaint': complaint})
