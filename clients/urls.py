
from django.urls import path, include
from .views import clients, client_create, client_update, client_detail, client_delete, contacts, contact_create, contact_update, contact_detail, contact_delete

app_name = 'clients'

urlpatterns = [
    path('', clients , name="clients"),
    path('nouveau/', client_create, name='create'),
    path('<int:pk>/modifier/', client_update, name='modifier'),
    path('<int:pk>', client_detail, name='detail'),
    path('<int:pk>/supprimer/', client_delete, name='delete'),
    path('contact/', contacts, name='contacts'),
    path('nouveau_contact/', contact_create, name='create_contact'),
    path('<int:pk>/modifier_contact/', contact_update, name='modifier_contact'),
    path('<int:pk>/detail_contact/', contact_detail, name='detail_contact'),
    path('<int:pk>/supprimer_contact/', contact_delete, name='delete_contact'),

]
