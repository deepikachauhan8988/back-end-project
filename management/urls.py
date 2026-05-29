# urls.py

from django.urls import path
from .views import (
    EmployeeRegisterView, 
    EmployeeLoginView, 
    EmployeeListView, 
    EmployeeDetailView,
    create_interview_question,
    get_random_question,
    get_questions_by_category,
    check_answer
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Register API
    path('register/', EmployeeRegisterView.as_view(), name='register'),

    # Login API
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),

    # Refresh Token API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('employee-list/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<str:regi_id>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Interview System APIs
    path('question/create/', create_interview_question, name='create-question'),
    path('question/random/', get_random_question, name='random-question'),
    path('question/category/<str:category>/', get_questions_by_category, name='questions-by-category'),
    path('question/check-answer/', check_answer, name='check-answer'),
]