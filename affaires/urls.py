
from django.urls import path, include
from .views import affaires, affaire_detail, affaire_create, affaire_update

app_name = 'affaires'

urlpatterns = [
    path('', affaires, name="affaires"),
    path('<int:pk>', affaire_detail, name='detail'),
    path('nouveau', affaire_create, name='create'),
    path('<int:pk>/modifier/', affaire_update, name='modifier'),
]
