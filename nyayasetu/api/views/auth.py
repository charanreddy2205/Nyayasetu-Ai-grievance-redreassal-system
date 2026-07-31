import logging
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.decorators import api_view, permission_classes

from api.serializers.auth import UserSerializer, RegisterSerializer
from api.services.auth_service import AuthService
from api.responses import success_response, error_response

logger = logging.getLogger(__name__)

class SessionView(APIView):
    """
    Checks active session state and outputs current credentials + CSRF token.
    """
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest) -> Response:
        csrf_token = get_token(request)
        if request.user.is_authenticated:
            serializer = UserSerializer(instance=request.user)
            data = serializer.data
            data["isAuthenticated"] = True
            data["csrfToken"] = csrf_token
            return Response(data)
        return Response({
            "isAuthenticated": False,
            "csrfToken": csrf_token
        })


class LoginView(APIView):
    """
    Processes authentication request and initializes user session.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request: HttpRequest) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response({
                    "success": False,
                    "message": "This account is inactive.",
                    "data": None,
                    "errors": None
                }, status=403)
            login(request, user)
            serializer = UserSerializer(instance=user)
            
            # Legacy wrapper support for frontend
            return Response({
                "success": True,
                "message": "Logged in successfully.",
                "user": serializer.data,
                "data": {"user": serializer.data}
            })
            
        return Response({
            "success": False,
            "message": "Invalid username or password.",
            "error": "Invalid username or password.",
            "data": None,
            "errors": None
        }, status=401)


class LogoutView(APIView):
    """
    Terminates active session and signs the user out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest) -> Response:
        logout(request)
        return Response({
            "success": True,
            "message": "Signed out successfully.",
            "data": {}
        })


class RegisterView(APIView):
    """
    Handles citizen registration requests.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'

    def post(self, request: HttpRequest) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = AuthService.register_citizen(
                username=serializer.validated_data["username"],
                first_name=serializer.validated_data["firstName"],
                last_name=serializer.validated_data["lastName"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            login(request, user)
            user_serializer = UserSerializer(instance=user)
            return Response({
                "success": True,
                "message": "Registered successfully.",
                "user": user_serializer.data,
                "data": {"user": user_serializer.data}
            }, status=201)
            
        return Response({
            "success": False,
            "message": "Validation failed.",
            "data": None,
            "errors": serializer.errors
        }, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf(request):
    """
    Return a CSRF token for the frontend to use in POST requests.
    """
    return Response({'csrfToken': get_token(request)})
