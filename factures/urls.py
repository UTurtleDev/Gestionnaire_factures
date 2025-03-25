
from django.urls import path, include
from .views import factures, facture_detail, facture_create, facture_update, facture_delete, reglement_create

app_name = 'factures'

urlpatterns = [
    path('', factures , name="factures"),
    path('nouvelle/', facture_create, name='create'),
    path('<int:pk>/modifier/', facture_update, name='modifier'),
    path('<int:pk>', facture_detail, name='detail'),
    path('<int:pk>/supprimer/', facture_delete, name='delete'),
    path('<int:pk>/reglement/', reglement_create, name='reglement'),
]
