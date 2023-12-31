from django.urls import path
from . import views
from .views import RegistrationView, LoginView, AdminRegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('adminregister', AdminRegistrationView.as_view(), name='admin_register'),
    path('toggle_like_movie/<int:movie_id>', views.toggle_like_movie, name='toggle_like_movie'),
    path('user/<str:username>', views.get_user_profile, name='user_profile'),
]