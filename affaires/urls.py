
from django.urls import path, include
from .views import affaires

app_name = 'affaires'

urlpatterns = [
    path('', affaires, name="affaires"),

]
