
from django.urls import path, include
from .views import clients, client_create

app_name = 'clients'

urlpatterns = [
    path('', clients , name="clients"),
    path('nouveau/', client_create, name='create'),
]
