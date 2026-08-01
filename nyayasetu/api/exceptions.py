import logging
from functools import wraps
from django.http import JsonResponse
from .responses import error_response, validation_error, permission_denied, not_found

logger = logging.getLogger(__name__)

class APIException(Exception):
    """
    Base exception for API errors.
    """
    status_code = 500
    
    def __init__(self, message: str, errors: list | dict | None = None):
        super().__init__(message)
        self.message = message
        self.errors = errors

class ValidationException(APIException):
    """
    Exception raised on field validation failures.
    """
    status_code = 400

class PermissionDeniedException(APIException):
    """
    Exception raised when access checks fail.
    """
    status_code = 403

class NotFoundException(APIException):
    """
    Exception raised when a database record is missing.
    """
    status_code = 404

def handle_api_exceptions(view_func):
    """
    Decorator to centrally catch APIExceptions and unexpected errors,
    preventing internal trace leakages and returning clean JSON responses.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValidationException as e:
            return validation_error(errors=e.errors or {}, message=e.message)
        except PermissionDeniedException as e:
            return permission_denied(message=e.message)
        except NotFoundException as e:
            return not_found(message=e.message)
        except APIException as e:
            return error_response(message=e.message, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected API error in {view_func.__name__}: {e}", exc_info=True)
            return error_response(message="An internal server error occurred.", status=500)
    return _wrapped


from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context) -> Response:
    """
    Standardizes DRF exception payloads into the uniform JSON wrapper format.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        errors = None
        message = str(exc)
        
        if response.status_code == 400:
            errors = response.data
            message = "Validation failed."
        elif isinstance(response.data, dict) and "detail" in response.data:
            message = response.data["detail"]
            
        response.data = {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors
        }
    else:
        # Catch our custom non-DRF exceptions
        if isinstance(exc, ValidationException):
            return validation_error(errors=exc.errors or {}, message=exc.message)
        elif isinstance(exc, PermissionDeniedException):
            return permission_denied(message=exc.message)
        elif isinstance(exc, NotFoundException):
            return not_found(message=exc.message)
        elif isinstance(exc, APIException):
            return error_response(message=exc.message, status=exc.status_code)

        logger.error(f"Uncaught server exception: {exc}", exc_info=exc)
        response = Response({
            "success": False,
            "message": "An internal server error occurred.",
            "data": None,
            "errors": None
        }, status=500)
        
    return response
