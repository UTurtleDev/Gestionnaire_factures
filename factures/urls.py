
from django.urls import path, include
from .views import factures, facture_detail, facture_create

app_name = 'factures'

urlpatterns = [
    path('', factures , name="factures"),
    path('nouvelle/', facture_create, name='create'),
    path('<int:pk>', facture_detail, name='detail'),
]
