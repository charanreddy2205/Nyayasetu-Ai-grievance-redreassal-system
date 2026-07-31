from django.urls import path
from . import views

urlpatterns = [
    path('', views.citizen_dashboard, name='citizen_dashboard'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    path('public/', views.public_dashboard, name='public_dashboard'),
]
