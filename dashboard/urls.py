
from django.urls import path
from .views import login, dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', login, name="login"),
    path('dashboard/', dashboard, name="dashboard")
]
