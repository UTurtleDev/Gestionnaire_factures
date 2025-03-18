
from django.urls import path, include
from .views import clients

app_name = 'clients'

urlpatterns = [
    path('', clients , name="clients"),
]
