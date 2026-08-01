from typing import Any
from rest_framework import serializers
from decimal import Decimal
from complaints.models import Complaint, ComplaintComment
from api.serializers.auth import UserSerializer
from api.serializers.department import DepartmentSerializer
from api.validators import validate_and_sanitize_upload

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer rendering progress updates comments.
    """
    author = UserSerializer(read_only=True)
    imageUrl = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    comment_text = serializers.CharField(source='comment_text')

    class Meta:
        model = ComplaintComment
        fields = ['id', 'comment_text', 'image', 'imageUrl', 'createdAt', 'author']

    def get_imageUrl(self, obj: ComplaintComment) -> str | None:
        return obj.image.url if obj.image else None

    def get_createdAt(self, obj: ComplaintComment) -> str:
        return obj.created_at.isoformat()


class ComplaintSerializer(serializers.ModelSerializer):
    """
    Read-only detailed serializer for Grievances.
    """
    created_by = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    assignedTo = UserSerializer(source='assigned_to', read_only=True)
    imageUrl = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    resolvedAt = serializers.SerializerMethodField()
    slaDeadline = serializers.SerializerMethodField()
    urgencyLevel = serializers.CharField(source='urgency_level', read_only=True)
    sentimentScore = serializers.FloatField(source='sentiment_score', read_only=True)
    escalationLevel = serializers.IntegerField(source='escalation_level', read_only=True)
    originalSlaHours = serializers.IntegerField(source='original_sla_hours', read_only=True)
    contactNumber = serializers.CharField(source='contact_number', read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'title', 'description', 'image', 'imageUrl', 'created_by', 
            'department', 'assignedTo', 'status', 'escalationLevel', 
            'urgencyLevel', 'sentimentScore', 'originalSlaHours', 'slaDeadline', 'createdAt', 
            'resolvedAt', 'address', 'city', 'state', 'pincode', 'latitude', 
            'longitude', 'contactNumber', 'summary'
        ]

    def get_imageUrl(self, obj: Complaint) -> str | None:
        return obj.image.url if obj.image else None

    def get_createdAt(self, obj: Complaint) -> str:
        return obj.created_at.isoformat()

    def get_resolvedAt(self, obj: Complaint) -> str | None:
        return obj.resolved_at.isoformat() if obj.resolved_at else None

    def get_slaDeadline(self, obj: Complaint) -> str | None:
        return obj.sla_deadline.isoformat() if obj.sla_deadline else None


class ComplaintCreateSerializer(serializers.ModelSerializer):
    """
    Serializer enforcing validations during lodging of grievances.
    """
    latitude = serializers.DecimalField(max_digits=20, decimal_places=15, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=20, decimal_places=15, required=False, allow_null=True)
    contact_number = serializers.CharField(max_length=15, required=False, allow_blank=True, allow_null=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Complaint._meta.get_field('department').remote_field.model.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Complaint
        fields = [
            'title', 'description', 'contact_number', 'address', 'city', 
            'state', 'pincode', 'latitude', 'longitude', 'department', 'image'
        ]

    def validate_image(self, value: Any) -> Any:
        if value:
            from django.core.exceptions import ValidationError
            try:
                return validate_and_sanitize_upload(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        return value

    def validate_latitude(self, value: Decimal | None) -> Decimal | None:
        if value is not None and not (-90 <= value <= 90):
            raise serializers.ValidationError("Latitude must be between -90.0 and 90.0 degrees.")
        return value

    def validate_longitude(self, value: Decimal | None) -> Decimal | None:
        if value is not None and not (-180 <= value <= 180):
            raise serializers.ValidationError("Longitude must be between -180.0 and 180.0 degrees.")
        return value
