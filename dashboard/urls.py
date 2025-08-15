
from django.urls import path
from .views import login, dashboard, chiffre_d_affaires

app_name = 'dashboard'

urlpatterns = [
    path('', login, name="login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/chiffre_d_affaires', chiffre_d_affaires, name="chiffre_d_affaires"),
]
