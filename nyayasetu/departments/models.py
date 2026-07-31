from django.db import models

class Department(models.Model):
    """
    Department model managing resolution SLA policies and transparency performance indexes.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    sla_hours = models.IntegerField(default=48)
    transparency_score = models.FloatField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['transparency_score']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(transparency_score__gte=0.0) & models.Q(transparency_score__lte=100.0),
                name='department_transparency_score_range'
            ),
            models.CheckConstraint(
                condition=models.Q(sla_hours__gt=0),
                name='department_sla_hours_positive'
            )
        ]

    def __str__(self) -> str:
        return self.name


class DepartmentKeyword(models.Model):
    """
    Keywords and weights mapping to departments for auto-routing calculations.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='keywords')
    word = models.CharField(max_length=100, help_text="Keyword word or synonym")
    weight = models.IntegerField(default=1, help_text="Weight impact score")

    class Meta:
        unique_together = ('department', 'word')
        indexes = [
            models.Index(fields=['word']),
        ]

    def __str__(self) -> str:
        return f"{self.word} ({self.department.name}, weight={self.weight})"
