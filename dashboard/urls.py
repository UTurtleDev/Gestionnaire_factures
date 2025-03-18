
from django.urls import path
from .views import login

app_name = 'dashboard'

urlpatterns = [
    path('', login, name="login"),
]
