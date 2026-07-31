import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(
    bind=True,
    max_retries=5,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,  # Max 10 mins backoff
    name='api.tasks.process_complaint_ai_task'
)
def process_complaint_ai_task(self, complaint_id: int) -> dict:
    """
    Celery background task running the full AI pipeline for a complaint.

    Steps:
        1. Fetch the complaint record from the database.
        2. Run the AIProcessingPipeline sequentially.
        3. Resolve a matching department and assigned officer.
        4. Write all AI output columns back to the Complaint model.
        5. Record an AuditLog entry for the AI processing event.

    Args:
        complaint_id: The database PK of the target Complaint record.

    Returns:
        A dict summary of the processing result.
    """
    try:
        from complaints.models import Complaint
        from departments.models import Department
        from api.models import AuditLog
        from ai.pipeline import AIProcessingPipeline
        from api.constants import (
            ROLE_CITIZEN, ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN
        )

        # Fetch target complaint
        try:
            complaint = Complaint.objects.select_related('department', 'assigned_to').get(pk=complaint_id)
        except Complaint.DoesNotExist:
            logger.error(f"[AITask] Complaint #{complaint_id} not found.")
            return {"error": f"Complaint #{complaint_id} not found."}

        description = complaint.description or ""

        # Execute the AI pipeline
        pipeline = AIProcessingPipeline()
        result = pipeline.process(complaint_id=complaint_id, text=description)

        # Resolve department from classification result
        department = None
        try:
            department = Department.objects.filter(name__iexact=result.department_name).first()
            if not department:
                # Fuzzy match: try partial name match
                department = Department.objects.filter(name__icontains=result.department_name.split()[0]).first()
            if not department:
                department = complaint.department or Department.objects.first()
        except Exception as e:
            logger.error(f"[AITask][Complaint #{complaint_id}] Department resolution failed: {e}")
            department = complaint.department

        # Resolve automatic assignee officer
        assigned_officer = complaint.assigned_to
        if department:
            officer_roles = [ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN]
            for role in officer_roles:
                officer = User.objects.filter(
                    department=department, role=role, is_active=True
                ).first()
                if officer:
                    assigned_officer = officer
                    break

        # Persist AI results back to the Complaint
        update_fields = []

        if result.urgency_level:
            complaint.urgency_level = result.urgency_level
            update_fields.append('urgency_level')

        if result.summary:
            complaint.summary = result.summary
            update_fields.append('summary')

        if department and not complaint.department:
            complaint.department = department
            update_fields.append('department')

        if assigned_officer and not complaint.assigned_to:
            complaint.assigned_to = assigned_officer
            update_fields.append('assigned_to')

        if update_fields:
            complaint.save(update_fields=update_fields)

        # Write immutable audit trail entry
        try:
            AuditLog.objects.create(
                action_type='complaint_created',
                performed_by=None,
                description=(
                    f"AI pipeline completed for Complaint #{complaint_id}: "
                    f"dept={result.department_name}, urgency={result.urgency_level}, "
                    f"sentiment={result.sentiment_score:.3f}, "
                    f"time={result.processing_ms:.1f}ms, fallback={result.fallback_used}"
                ),
                object_id=complaint_id,
                object_type='Complaint'
            )
        except Exception as e:
            logger.warning(f"[AITask][Complaint #{complaint_id}] Audit log write failed: {e}")

        return {
            "complaint_id": complaint_id,
            "department": result.department_name,
            "urgency": result.urgency_level,
            "sentiment": result.sentiment_score,
            "processing_ms": result.processing_ms,
            "fallback_used": result.fallback_used,
        }

    except Exception as exc:
        logger.error(
            f"[AITask][Complaint #{complaint_id}] Unhandled error: {exc}",
            exc_info=True
        )
        return {"error": str(exc), "complaint_id": complaint_id}
