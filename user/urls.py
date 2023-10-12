from django.urls import path
from . import views
from .views import RegistrationView
from .views import LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
