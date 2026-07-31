from rest_framework import serializers
from departments.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer mapping Department attributes.
    """
    transparencyScore = serializers.FloatField(source='transparency_score', read_only=True)
    slaHours = serializers.IntegerField(source='sla_hours', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'slaHours', 'transparencyScore']
