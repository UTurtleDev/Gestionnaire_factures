
from django.urls import path, include
from .views import factures, facture_detail, facture_create, facture_update, facture_delete, reglement_create, reglements, reglement_detail, reglement_update, reglement_delete

app_name = 'factures'

urlpatterns = [
    path('', factures , name="factures"),
    path('nouvelle/', facture_create, name='create'),
    path('<int:pk>/modifier/', facture_update, name='modifier'),
    path('<int:pk>', facture_detail, name='detail'),
    path('<int:pk>/supprimer/', facture_delete, name='delete'),
    path('reglements/', reglements, name='reglements'),
    path('<int:pk>/reglement/', reglement_create, name='reglement'),
    path('<int:pk>/reglement/modifier/', reglement_update, name='reglement_modifier'),
    path('<int:pk>/detail_reglement/', reglement_detail, name='reglement_detail'),
    path('<int:pk>/supprimer_reglement/', reglement_delete, name='reglement_delete')
]
