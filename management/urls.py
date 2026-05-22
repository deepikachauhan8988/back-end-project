# urls.py

from django.urls import path
from .views import EmployeeRegisterView, EmployeeLoginView, EmployeeListView, EmployeeDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Register API
    path('register/', EmployeeRegisterView.as_view(), name='register'),

    # Login API
    path('employee-login/', EmployeeLoginView.as_view(), name='employee-login'),

    # Refresh Token API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('employee-list/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<str:regi_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
]