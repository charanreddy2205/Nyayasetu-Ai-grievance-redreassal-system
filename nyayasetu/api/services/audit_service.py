from api.models import AuditLog
from typing import Any

class AuditService:
    """
    Service layer providing helper utilities to log transactions.
    """
    
    @staticmethod
    def log_action(
        action_type: str,
        performed_by: Any,
        description: str,
        object_id: int | None = None,
        object_type: str | None = None
    ) -> AuditLog:
        """
        Inserts a new AuditLog transaction record.

        Args:
            action_type: Category of action.
            performed_by: User account triggering the action.
            description: Detailed text description.
            object_id: Target database PK.
            object_type: Class name of target record.
        """
        return AuditLog.objects.create(
            action_type=action_type,
            performed_by=performed_by,
            description=description,
            object_id=object_id,
            object_type=object_type
        )
