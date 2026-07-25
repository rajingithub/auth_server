from django.urls import path
from accounts.views.auth_view import AuthView
from accounts.views.user_view import UserCreateView, UserListView
from accounts.views.application_view import ApplicationCreateView

urlpatterns = [
    path('token', AuthView.as_view()),
    path('create', UserCreateView.as_view()),
    path('list', UserListView.as_view()),
    path('application/create', ApplicationCreateView.as_view()),
]