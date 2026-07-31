from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.services.dashboard_service import DashboardService
from api.serializers.dashboard import DashboardStatsSerializer
from django.http import HttpRequest

class DashboardStatsView(APIView):
    """
    APIView returning dashboard analytics stats metrics.
    """
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest) -> Response:
        stats = DashboardService.get_dashboard_stats(request.user)
        serializer = DashboardStatsSerializer(instance=stats)
        # Return the serialized data directly for compatibility
        return Response(serializer.data)
