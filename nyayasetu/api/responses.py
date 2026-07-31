from django.http import JsonResponse
from typing import Any, Dict, Optional, Union

def success_response(
    data: Any,
    message: Optional[str] = None,
    status: int = 200
) -> JsonResponse:
    """
    Returns a unified JSON success response.
    """
    payload = {"success": True}
    if message is not None:
        payload["message"] = message
        
    if isinstance(data, dict):
        payload.update(data)
    else:
        payload["data"] = data
        
    return JsonResponse(payload, status=status)

def error_response(
    message: str,
    status: int = 500,
    errors: Optional[Union[Dict[str, Any], list]] = None
) -> JsonResponse:
    """
    Returns a unified JSON error response.
    """
    payload = {
        "success": False,
        "error": message
    }
    if errors is not None:
        payload["errors"] = errors
        
    return JsonResponse(payload, status=status)

def validation_error(
    errors: Union[Dict[str, Any], list],
    message: str = "Validation failed."
) -> JsonResponse:
    """
    Returns a standard 400 Validation Error response.
    """
    return error_response(message, status=400, errors=errors)

def permission_denied(
    message: str = "You do not have permission to perform this action."
) -> JsonResponse:
    """
    Returns a standard 403 Permission Denied response.
    """
    return error_response(message, status=403)

def not_found(
    message: str = "The requested resource was not found."
) -> JsonResponse:
    """
    Returns a standard 404 Not Found response.
    """
    return error_response(message, status=404)
