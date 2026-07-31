from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model supporting roles and department assignments.
    """
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('staff', 'Staff'),
        ('hod', 'Head of Department'),
        ('district_officer', 'District Officer'),
        ('state_admin', 'State Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )

    class Meta:
        indexes = [
            models.Index(fields=['role']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(role__in=['citizen', 'staff', 'hod', 'district_officer', 'state_admin']),
                name='user_role_check'
            )
        ]

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
