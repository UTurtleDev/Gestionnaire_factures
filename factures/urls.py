
from django.urls import path, include
from .views import factures

app_name = 'factures'

urlpatterns = [
    path('', factures , name="factures"),
]
