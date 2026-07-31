from typing import Any
from complaints.models import Complaint, ComplaintComment
from api.exceptions import PermissionDeniedException, NotFoundException, ValidationException
from api.constants import ROLE_CITIZEN, ROLE_STATE_ADMIN

class CommentService:
    """
    Service handling creation of comments and verification of user permissions.
    """
    
    @staticmethod
    def add_comment(
        user: Any,
        complaint_id: int,
        comment_text: str,
        image: Any = None
    ) -> ComplaintComment:
        """
        Creates a text/photo comment on a complaint, verifying access boundaries.
        """
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            raise NotFoundException(f"Grievance #{complaint_id} not found.")
            
        # Access permission check
        has_access = (
            complaint.created_by == user or
            complaint.assigned_to == user or
            user.role == ROLE_STATE_ADMIN or
            (user.role != ROLE_CITIZEN and user.department == complaint.department)
        )
        if not has_access:
            raise PermissionDeniedException("You do not have access to add comments to this complaint.")
            
        if not comment_text:
            raise ValidationException("Comment text is a required field.")
            
        comment = ComplaintComment(
            complaint=complaint,
            author=user,
            comment_text=comment_text,
            image=image
        )
        comment.save()
        from api.services.audit_service import AuditService
        AuditService.log_action(
            action_type='status_updated',
            performed_by=user,
            description="Added a comment response.",
            object_id=complaint.id,
            object_type='Complaint'
        )
        return comment
