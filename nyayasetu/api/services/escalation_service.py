import logging
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import F
from complaints.models import Complaint
from escalation.models import EscalationLog
from django.contrib.auth import get_user_model
from api.constants import (
    STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_ESCALATED, STATUS_ADMINISTRATIVE_FAILURE,
    ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN, MAX_ESCALATION_LEVEL, TRANSPARENCY_PENALTY
)

logger = logging.getLogger(__name__)
User = get_user_model()

class EscalationService:
    """
    Service layer executing automated SLA escalation workflows.
    """
    
    @staticmethod
    def escalate_complaints() -> int:
        """
        Queries overdue complaints, loops atomic reassignments, computes half-life deadlines,
        and applies transparency score penalties to administrative failures.

        Returns:
            Count of complaints processed.
        """
        now = timezone.now()
        overdue_complaints = Complaint.objects.filter(
            status__in=[STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_ESCALATED],
            sla_deadline__lt=now
        )
        
        count = 0
        for complaint in overdue_complaints:
            try:
                with transaction.atomic():
                    complaint.refresh_from_db()
                    if complaint.sla_deadline >= now:
                        continue
                        
                    current_level = complaint.escalation_level
                    
                    if current_level < MAX_ESCALATION_LEVEL:
                        new_level = current_level + 1
                        
                        next_role = None
                        if new_level == 1:
                            next_role = ROLE_HOD
                        elif new_level == 2:
                            next_role = ROLE_DISTRICT_OFFICER
                        elif new_level == 3:
                            next_role = ROLE_STATE_ADMIN
                            
                        # Locate new assignee
                        new_assignee = User.objects.filter(
                            role=next_role,
                            department=complaint.department,
                            is_active=True
                        ).first()
                        
                        if not new_assignee:
                            new_assignee = User.objects.filter(role=next_role, is_active=True).first()
                            
                        # Halve SLA remaining hours per level
                        if complaint.original_sla_hours:
                            new_sla_hours = complaint.original_sla_hours / (2 ** new_level)
                        else:
                            new_sla_hours = 24
                            
                        new_deadline = now + timedelta(hours=new_sla_hours)
                        
                        complaint.escalation_level = new_level
                        complaint.sla_deadline = new_deadline
                        complaint.status = STATUS_ESCALATED
                        if new_assignee:
                            complaint.assigned_to = new_assignee
                        complaint.save()
                        
                        EscalationLog.objects.create(
                            complaint=complaint,
                            escalated_to=new_assignee if new_assignee else complaint.assigned_to,
                            reason=f"SLA breached. Escalated to Level {new_level} ({next_role})."
                        )
                        from api.services.audit_service import AuditService
                        AuditService.log_action(
                            action_type='escalated',
                            performed_by=None,
                            description=f"Automated SLA breach escalation. Level {new_level} reached. Reassigned to {new_assignee.username if new_assignee else 'unassigned'}.",
                            object_id=complaint.id,
                            object_type='Complaint'
                        )
                        count += 1
                    else:
                        complaint.status = STATUS_ADMINISTRATIVE_FAILURE
                        complaint.save()
                        
                        from api.services.audit_service import AuditService
                        AuditService.log_action(
                            action_type='status_updated',
                            performed_by=None,
                            description="Grievance transitioned to administrative failure due to max SLA breach level limit.",
                            object_id=complaint.id,
                            object_type='Complaint'
                        )
                        
                        if complaint.department:
                            # Apply penalty to department transparency index score
                            complaint.department.transparency_score = F('transparency_score') - TRANSPARENCY_PENALTY
                            complaint.department.save()
                            count += 1
            except Exception as e:
                logger.error(f"Error escalating complaint ID {complaint.id}: {e}", exc_info=True)
                
        return count
