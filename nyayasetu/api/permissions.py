from rest_framework import permissions
from api.constants import ROLE_CITIZEN, ROLE_STATE_ADMIN, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STAFF
from typing import Any

class IsCitizen(permissions.BasePermission):
    """
    Allows access only to citizen accounts.
    """
    def has_permission(self, request: Any, view: Any) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_CITIZEN)

class IsOfficer(permissions.BasePermission):
    """
    Allows access to official department representatives.
    """
    def has_permission(self, request: Any, view: Any) -> bool:
        allowed_roles = [ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER, ROLE_STATE_ADMIN]
        return bool(request.user and request.user.is_authenticated and request.user.role in allowed_roles)

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to state admins.
    """
    def has_permission(self, request: Any, view: Any) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_STATE_ADMIN)

class IsComplaintParticipant(permissions.BasePermission):
    """
    Object-level permission check evaluating access to a specific grievance.
    """
    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
            
        is_citizen_owner = obj.created_by_id == request.user.id
        is_current_owner = hasattr(obj, 'current_owner_id') and obj.current_owner_id == request.user.id
        is_dept_officer = request.user.role in [ROLE_STAFF, ROLE_HOD, ROLE_DISTRICT_OFFICER] and obj.department_id == request.user.department_id
        is_state_admin = request.user.role == ROLE_STATE_ADMIN
        
        # Read operations (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return is_citizen_owner or is_current_owner or is_dept_officer or is_state_admin
            
        # Write operations
        # Allow citizen creator to post comments
        if getattr(view, 'action', None) == 'post_comment':
            return is_citizen_owner or is_current_owner
            
        # Only the current owner can update status, modify fields, delete, etc.
        return is_current_owner
