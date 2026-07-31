class SecurityHeadersMiddleware:
    """
    Middleware to inject robust security headers into all outgoing HTTP responses
    to prevent XSS, clickjacking, mime sniffing, and framing attacks.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enforce frame options protection
        response['X-Frame-Options'] = 'DENY'
        
        # Configure Content-Security-Policy (CSP)
        # Allows self host, external image tiles (OSM), and fonts.
        # Safe inline scripts are allowed for the demonstration UI, but restricted.
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; "
            "img-src 'self' data: blob: https://*.tile.openstreetmap.org https://unpkg.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' https://nominatim.openstreetmap.org; "
            "frame-ancestors 'none';"
        )
        
        # Enforce Permissions-Policy
        response['Permissions-Policy'] = 'geolocation=(self), camera=(), microphone=(), payment=()'
        
        return response
