from django.urls import path

from rest_framework.authtoken import views

from .views import UserDetailAPI,RegisterUserAPIView

urlpatterns = [
    path('whoami', UserDetailAPI.as_view(), name='whoami'),
    path('login', views.obtain_auth_token, name='login'),
    path('register', RegisterUserAPIView.as_view(), name='register'),
]