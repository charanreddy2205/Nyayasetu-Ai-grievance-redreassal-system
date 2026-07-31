from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from departments.models import Department
from api.serializers.department import DepartmentSerializer
from api.services.department_service import DepartmentService
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet listing available departments.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return DepartmentService.list_departments()

    @method_decorator(cache_page(60 * 60 * 24))  # Cache for 24 hours
    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Departments retrieved.",
            "departments": serializer.data,
            "data": {"departments": serializer.data}
        })
