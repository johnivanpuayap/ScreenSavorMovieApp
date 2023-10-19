from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('movies/', include('movie.urls')),
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', RedirectView.as_view(url='/movies/')),
]