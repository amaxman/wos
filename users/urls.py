from django.urls import path
from .views import LoginView,LoginBySessionView

urlpatterns = [
    path('login', LoginView.as_view(), name='rest-login'),
    path('login_token', LoginBySessionView.as_view(), name='rest-login-token'),
]
