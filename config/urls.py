from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search, name='search'),
    path('', include('dashboard.urls')),
    path('clients/', include('clients.urls')),
    path('factures/', include('factures.urls')),
    path('affaires/', include('affaires.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# En développement, servir les fichiers media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
