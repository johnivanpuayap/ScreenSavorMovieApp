from django.urls import path
from . import views
from .views import RegistrationView, LoginView, AdminRegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('adminregister', AdminRegistrationView.as_view(), name='register'),
]
