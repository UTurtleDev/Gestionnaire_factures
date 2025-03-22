
from django.urls import path, include
from .views import clients, client_create, client_update, client_detail, client_delete

app_name = 'clients'

urlpatterns = [
    path('', clients , name="clients"),
    path('nouveau/', client_create, name='create'),
    path('<int:pk>/modifier/', client_update, name='modifier'),
    path('<int:pk>', client_detail, name='detail'),
    path('<int:pk>/supprimer/', client_delete, name='delete'),
]
