from django.db import models
from django.conf import settings
from django.utils import timezone
from typing import Any

class SoftDeleteQuerySet(models.QuerySet):
    """
    QuerySet overriding delete to perform soft deletions.
    """
    def delete(self) -> tuple[int, dict[str, int]]:
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        return super().delete()

class SoftDeleteManager(models.Manager):
    """
    Manager returning only non-deleted objects by default.
    """
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    """
    Abstract base class providing soft-deletion support.
    """
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs) -> None:
        """
        Soft deletes the instance.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self) -> None:
        """
        Restores a soft-deleted instance.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


class AuditLog(models.Model):
    """
    Immutable database-level audit log recording critical user or system actions.
    """
    ACTION_CHOICES = (
        ('complaint_created', 'Complaint Created'),
        ('status_updated', 'Status Updated'),
        ('officer_assigned', 'Officer Assigned'),
        ('escalated', 'Escalated'),
        ('user_role_changed', 'User Role Changed'),
        ('department_updated', 'Department Updated'),
        ('record_deleted', 'Record Deleted'),
    )

    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_actions'
    )
    object_id = models.IntegerField(blank=True, null=True)
    object_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action_type', 'created_at']),
            models.Index(fields=['object_type', 'object_id']),
        ]

    def __str__(self) -> str:
        return f"{self.action_type} by {self.performed_by} at {self.created_at}"
