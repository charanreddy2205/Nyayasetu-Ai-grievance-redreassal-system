from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

class LivenessProbeView(APIView):
    """
    K8s Liveness Probe endpoint. Checks if application server is running.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "message": "Application is live."})

class ReadinessProbeView(APIView):
    """
    K8s Readiness Probe endpoint. Checks if database & dependencies are reachable.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Check DB connection
            connection.ensure_connection()
            return Response({"status": "ok", "message": "Ready to serve traffic."})
        except Exception as e:
            return Response(
                {"status": "error", "message": "Database not reachable.", "details": str(e)}, 
                status=503
            )
