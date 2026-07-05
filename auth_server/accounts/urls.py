from django.urls import path
from accounts.views.auth_view import AuthView

urlpatterns = [
    path('token', AuthView.as_view())
]