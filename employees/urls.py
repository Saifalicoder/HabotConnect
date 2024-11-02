from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list_create, name='employee-list-create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),
]
