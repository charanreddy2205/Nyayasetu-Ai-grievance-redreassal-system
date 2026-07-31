from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_complaint, name='create_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('assigned/', views.assigned_complaints, name='assigned_complaints'),
    path('detail/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('update-status/<int:pk>/', views.update_complaint_status, name='update_complaint_status'),
]
