from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('clients/', include('clients.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
