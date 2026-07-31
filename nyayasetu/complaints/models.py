from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from api.models import SoftDeleteModel

class Complaint(SoftDeleteModel):
    """
    Core complaint model inheriting SoftDeleteModel.
    Protects relation deletions, and defines range and choice check constraints.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
        ('administrative_failure', 'Administrative Failure'),
    )

    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    
    # Cascade Deletes Prevention
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='complaints'
    )
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.PROTECT, 
        related_name='complaints'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        related_name='assigned_complaints'
    )
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    escalation_level = models.IntegerField(default=0)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='low')
    original_sla_hours = models.IntegerField(blank=True, null=True)
    sla_deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    # Location Details
    address = models.TextField(blank=True, null=True, help_text="Street address or landmark")
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number for updates")

    summary = models.TextField(blank=True, null=True, help_text="AI-generated summary of the complaint")

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['sla_deadline']),
            models.Index(fields=['urgency_level']),
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            # Composite index for scheduler scan updates
            models.Index(fields=['status', 'sla_deadline'], name='complaint_status_sla_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=['pending', 'in_progress', 'resolved', 'escalated', 'administrative_failure']),
                name='complaint_status_check'
            ),
            models.CheckConstraint(
                condition=models.Q(urgency_level__in=['low', 'medium', 'high', 'critical']),
                name='complaint_urgency_check'
            ),
            # Lat/Long coordinate validity range checks
            models.CheckConstraint(
                condition=models.Q(latitude__gte=-90.0) & models.Q(latitude__lte=90.0),
                name='complaint_latitude_range'
            ),
            models.CheckConstraint(
                condition=models.Q(longitude__gte=-180.0) & models.Q(longitude__lte=180.0),
                name='complaint_longitude_range'
            )
        ]

    def save(self, *args, **kwargs) -> None:
        is_new = not self.pk
        
        if is_new:
            # Set SLA deadline based on department if not set
            if self.department and not self.sla_deadline:
                self.original_sla_hours = self.department.sla_hours
                self.sla_deadline = timezone.now() + timedelta(hours=self.original_sla_hours)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} - {self.status}"


class ComplaintComment(SoftDeleteModel):
    """
    Comment model mapping citizen/officer timeline text updates.
    """
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    comment_text = models.TextField()
    image = models.ImageField(upload_to='complaints/comments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on #{self.complaint.id} at {self.created_at}"
