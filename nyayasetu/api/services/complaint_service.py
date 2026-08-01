from typing import Any
import logging
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from complaints.models import Complaint
from departments.models import Department
from api.constants import (
    STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_RESOLVED, STATUS_ESCALATED, 
    ROLE_CITIZEN, ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN,
    DEFAULT_SLA_HOURS
)
from api.services.ai_service import AIService
from api.exceptions import ValidationException, PermissionDeniedException, NotFoundException

logger = logging.getLogger(__name__)
User = get_user_model()

class ComplaintService:
    """
    Service encapsulating operations on the Complaint model.
    Handles creations, status updates, permissions filtering, and query optimizations.
    """
    
    @staticmethod
    def resolve_assigned_officer(department: Department | None):
        """Resolve the best available officer for a department."""
        if not department:
            return None

        officer_roles = [ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN]
        for role in officer_roles:
            officer = User.objects.filter(
                department=department,
                role=role,
                is_active=True
            ).first()
            if officer:
                return officer

        # Fall back to any non-citizen officer in the department
        return User.objects.filter(
            department=department,
            is_active=True
        ).exclude(role=ROLE_CITIZEN).first()

    @staticmethod
    def get_complaints_list(
        user: Any,
        overdue_only: bool = False,
        status_filter: str | None = None
    ) -> list[Complaint]:
        """
        Retrieves complaints based on the user's role with optimized select_related.
        """
        now = timezone.now()
        
        # Optimize queries using select_related to solve N+1 problems
        base_query = Complaint.objects.select_related('department', 'assigned_to', 'created_by')
        
        if user.role == ROLE_CITIZEN:
            complaints = base_query.filter(created_by=user)
        elif user.role == ROLE_STATE_ADMIN:
            complaints = base_query.all()
        else:
            # Department officers (Staff, HOD, DO) read their department complaints
            if user.department:
                complaints = base_query.filter(department=user.department)
            else:
                complaints = base_query.none()

        if overdue_only:
            complaints = complaints.filter(
                sla_deadline__lt=now
            ).exclude(status__in=[STATUS_RESOLVED, 'administrative_failure'])

        if status_filter:
            complaints = complaints.filter(status=status_filter)

        return complaints.order_by('-created_at')

    @staticmethod
    def get_complaint_details(user: Any, complaint_id: int) -> tuple[Complaint, Any, Any]:
        """
        Fetches full complaint details. Verifies read permissions.
        """
        try:
            complaint = Complaint.objects.select_related(
                'department', 'assigned_to', 'created_by'
            ).get(pk=complaint_id)
        except Complaint.DoesNotExist:
            raise NotFoundException(f"Grievance #{complaint_id} not found.")

        # Access check based on hierarchical visibility
        has_access = False
        if complaint.created_by_id == user.id or complaint.assigned_to_id == user.id:
            has_access = True
        elif user.role == ROLE_STATE_ADMIN and complaint.escalation_level >= 3:
            has_access = True
        elif user.role != ROLE_CITIZEN and user.department_id == complaint.department_id:
            if user.role == ROLE_STAFF and complaint.escalation_level >= 0:
                has_access = True
            elif user.role == ROLE_HOD and complaint.escalation_level >= 1:
                has_access = True
            elif user.role == ROLE_DISTRICT_OFFICER and complaint.escalation_level >= 2:
                has_access = True
        if not has_access:
            raise PermissionDeniedException("You do not have access to view this complaint.")

        # Optimize comments and author loads using prefetch_related
        comments = complaint.comments.select_related('author').order_by('created_at')
        logs = complaint.escalation_logs.select_related('escalated_to').order_by('escalated_at')

        return complaint, comments, logs

    @staticmethod
    @transaction.atomic
    def create_complaint(
        user: Any,
        title: str,
        description: str,
        contact_number: str | None = None,
        address: str | None = None,
        city: str | None = None,
        state: str | None = None,
        pincode: str | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
        department_id: int | None = None,
        image: Any = None
    ) -> Complaint:
        """
        Lodge complaint service. Resolves auto department categorisation,
        sentiment urgency evaluation, summary abstraction, and routes assignee.
        """
        if not title or not description:
            raise ValidationException("Title and description are required fields.")

        # 1. Resolve Department (explicit selection or best-available fallback)
        department = None
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                logger.warning(f"Department ID {department_id} not found, using first available.")

        if not department:
            department = Department.objects.first()

        if not department:
            raise ValidationException("No default department is configured in the database.")

        # 2. Calculate SLA deadlines from department config
        sla_hours = department.sla_hours if department else DEFAULT_SLA_HOURS
        sla_deadline = timezone.now() + timedelta(hours=sla_hours)

        # 3. Save complaint IMMEDIATELY with defaults for AI columns
        # AI pipeline runs asynchronously to avoid blocking the request thread
        assigned_officer = ComplaintService.resolve_assigned_officer(department)

        complaint = Complaint(
            title=title,
            description=description,
            contact_number=contact_number,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            latitude=latitude,
            longitude=longitude,
            image=image,
            created_by=user,
            department=department,
            assigned_to=assigned_officer,
            urgency_level='low',     # AI will update this asynchronously
            summary='',              # AI will populate this asynchronously
            original_sla_hours=sla_hours,
            sla_deadline=sla_deadline,
            status=STATUS_PENDING
        )
        complaint.save()

        # 4. Dispatch AI background task (non-blocking)
        try:
            from api.tasks import process_complaint_ai_task
            is_auto_routed = (department_id is None)
            process_complaint_ai_task.delay(complaint.id, auto_routed=is_auto_routed)
            logger.info(f"[ComplaintService] AI task queued for Complaint #{complaint.id}, auto_routed={is_auto_routed}")
        except Exception as e:
            # Task dispatch failure must NEVER block complaint creation
            logger.error(f"[ComplaintService] Failed to queue AI task for Complaint #{complaint.id}: {e}")

        from api.services.audit_service import AuditService
        AuditService.log_action(
            action_type='complaint_created',
            performed_by=user,
            description=f"Grievance created: '{title}' under department '{department.name}'.",
            object_id=complaint.id,
            object_type='Complaint'
        )
        if complaint.assigned_to:
            AuditService.log_action(
                action_type='officer_assigned',
                performed_by=user,
                description=f"Grievance auto-assigned to officer {complaint.assigned_to.username}.",
                object_id=complaint.id,
                object_type='Complaint'
            )
        else:
            logger.warning(f"Complaint #{complaint.id} created without an assigned officer.")
        return complaint

    @staticmethod
    @transaction.atomic
    def update_status(user: Any, complaint_id: int, status: str) -> Complaint:
        """
        Updates complaint status. Restricted to the assigned officer.
        """
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            raise NotFoundException(f"Grievance #{complaint_id} not found.")

        if complaint.assigned_to != user:
            raise PermissionDeniedException("You are not authorized to update this complaint status.")

        if status not in [STATUS_IN_PROGRESS, STATUS_RESOLVED]:
            raise ValidationException("Invalid status target.")

        complaint.status = status
        if status == STATUS_RESOLVED:
            complaint.resolved_at = timezone.now()
            
        complaint.save()
        from api.services.audit_service import AuditService
        AuditService.log_action(
            action_type='status_updated',
            performed_by=user,
            description=f"Status transitioned to '{status}'.",
            object_id=complaint.id,
            object_type='Complaint'
        )
        return complaint
