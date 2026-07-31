from typing import Any
import logging
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from api.exceptions import ValidationException
from api.constants import ROLE_CITIZEN

logger = logging.getLogger(__name__)
User = get_user_model()

class AuthService:
    """
    Service handling user registration validation policies.
    """
    
    @staticmethod
    def register_citizen(
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> Any:
        """
        Registers a new citizen user after running format validation policies
        and password validation checks.
        """
        if not (username and first_name and last_name and email and password):
            raise ValidationException("All registration fields are required.")
            
        # 1. Format validation checks
        try:
            validate_email(email)
        except ValidationError as e:
            raise ValidationException(f"Email structure violation: {', '.join(e.messages)}")
            
        if User.objects.filter(username=username).exists():
            raise ValidationException("Username is already registered.")
            
        if User.objects.filter(email=email).exists():
            raise ValidationException("Email is already registered.")
            
        # 2. Enforce standard password validator policy
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationException(f"Password policy violation: {', '.join(e.messages)}")
            
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role=ROLE_CITIZEN
            )
            from api.services.audit_service import AuditService
            AuditService.log_action(
                action_type='user_role_changed',
                performed_by=user,
                description=f"Citizen registration for {username}.",
                object_id=user.id,
                object_type='User'
            )
            return user
        except Exception as e:
            logger.error(f"Error creating user account: {e}", exc_info=True)
            raise ValidationException("An error occurred while creating the citizen account.")
