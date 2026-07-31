import logging
from functools import wraps
from django.http import JsonResponse
from django.core.cache import cache

logger = logging.getLogger(__name__)

def rate_limit(key_prefix: str, limit: int, period: int):
    """
    Decorator for simple rate limiting utilizing Django cache framework.

    Args:
        key_prefix: Context prefix for the rate limit category.
        limit: Maximum allowed requests.
        period: Time window size in seconds.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                ident = f"user_{request.user.id}"
            else:
                ident = f"ip_{request.META.get('REMOTE_ADDR')}"
                
            cache_key = f"rate_limit_{key_prefix}_{ident}"
            request_count = cache.get(cache_key, 0)
            
            if request_count >= limit:
                logger.warning(f"Rate limit hit for {key_prefix} by {ident}")
                return JsonResponse({"error": "Rate limit exceeded. Please try again later."}, status=429)
                
            cache.set(cache_key, request_count + 1, period)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
