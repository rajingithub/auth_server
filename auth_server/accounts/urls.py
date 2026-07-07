from django.urls import path
from accounts.views.auth_view import AuthView
from accounts.views.user_view import UserCreateView

urlpatterns = [
    path('token', AuthView.as_view()),
    path('create', UserCreateView.as_view())
]