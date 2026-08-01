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
        if request.user.role == ROLE_STATE_ADMIN:
            return True
        if request.user.role == ROLE_CITIZEN:
            return obj.created_by_id == request.user.id
        return obj.department_id == request.user.department_id
