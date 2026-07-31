from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r'complaints', views.ComplaintViewSet, basename='complaint')
router.register(r'departments', views.DepartmentViewSet, basename='department')

# Legacy route mapping to keep frontend integration working without edits
legacy_patterns = [
    path('auth/csrf/', views.get_csrf, name='api_csrf'),
    path('auth/session/', views.SessionView.as_view(), name='api_session'),
    path('auth/login/', views.LoginView.as_view(), name='api_login'),
    path('auth/logout/', views.LogoutView.as_view(), name='api_logout'),
    path('auth/register/', views.RegisterView.as_view(), name='api_register'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='api_dashboard_stats'),
    path('geocode/reverse/', views.ReverseGeocodeView.as_view(), name='api_reverse_geocode'),
    path('departments/', views.DepartmentViewSet.as_view({'get': 'list'}), name='api_departments'),
    path('complaints/', views.ComplaintViewSet.as_view({'get': 'list'}), name='api_complaints'),
    path('complaints/create/', views.ComplaintViewSet.as_view({'post': 'create'}), name='api_complaint_create'),
    path('complaints/<int:pk>/', views.ComplaintViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='api_complaint_detail'),
    path('complaints/<int:pk>/status/', views.ComplaintViewSet.as_view({'post': 'patch_status', 'patch': 'patch_status'}), name='api_complaint_status'),
    path('complaints/<int:pk>/comments/', views.ComplaintViewSet.as_view({'post': 'post_comment'}), name='api_complaint_comment_create'),
    path('health/liveness/', views.LivenessProbeView.as_view(), name='api_health_liveness'),
    path('health/readiness/', views.ReadinessProbeView.as_view(), name='api_health_readiness'),
]

# Versioned API layout patterns
v1_patterns = [
    path('', include(router.urls)),
    path('auth/csrf/', views.get_csrf, name='v1_csrf'),
    path('auth/session/', views.SessionView.as_view(), name='v1_session'),
    path('auth/login/', views.LoginView.as_view(), name='v1_login'),
    path('auth/logout/', views.LogoutView.as_view(), name='v1_logout'),
    path('auth/register/', views.RegisterView.as_view(), name='v1_register'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='v1_dashboard_stats'),
    path('geocode/reverse/', views.ReverseGeocodeView.as_view(), name='v1_reverse_geocode'),
    path('health/liveness/', views.LivenessProbeView.as_view(), name='v1_health_liveness'),
    path('health/readiness/', views.ReadinessProbeView.as_view(), name='v1_health_readiness'),
]

urlpatterns = [
    # OpenAPI Schema generation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Version 1 Namespace
    path('v1/', include(v1_patterns)),
    # Default namespace mapped directly to legacy patterns
    path('', include(legacy_patterns)),
]
