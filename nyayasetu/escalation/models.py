from django.db import models
from django.conf import settings

class EscalationLog(models.Model):
    """
    Log mapping timeline event transitions when SLAs are breached.
    """
    complaint = models.ForeignKey('complaints.Complaint', on_delete=models.CASCADE, related_name='escalation_logs')
    escalated_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='escalations_received',
        null=True,
        blank=True
    )
    reason = models.TextField()
    escalated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-escalated_at']
        indexes = [
            models.Index(fields=['escalated_at']),
        ]

    def __str__(self) -> str:
        return f"Escalation for {self.complaint.title} to {self.escalated_to}"
