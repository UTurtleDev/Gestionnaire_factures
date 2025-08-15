
from django.urls import path, include
from .views import affaires, affaire_detail, affaire_create, affaire_update, affaire_delete, client_contacts_api

app_name = 'affaires'

urlpatterns = [
    path('', affaires, name="affaires"),
    path('<int:pk>', affaire_detail, name='detail'),
    path('nouveau', affaire_create, name='create'),
    path('<int:pk>/modifier/', affaire_update, name='modifier'),
    path('<int:pk>/supprimer/', affaire_delete, name='delete'),
    path('api/client-contacts/<int:client_id>/', client_contacts_api, name='client_contacts_api'),
]
