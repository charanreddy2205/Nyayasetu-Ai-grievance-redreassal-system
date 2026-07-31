from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for rendering User profile details.
    """
    departmentName = serializers.CharField(source='department.name', read_only=True)
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'role', 'department', 'departmentName']
        read_only_fields = ['id', 'role', 'department', 'departmentName']


class RegisterSerializer(serializers.Serializer):
    """
    Serializer handling user registration fields validation.
    """
    username = serializers.CharField(max_length=150)
    firstName = serializers.CharField(max_length=150)
    lastName = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value: str) -> str:
        validate_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already registered.")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value
