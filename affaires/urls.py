
from django.urls import path, include
from .views import affaires, affaire_detail

app_name = 'affaires'

urlpatterns = [
    path('', affaires, name="affaires"),
    path('<int:pk>', affaire_detail, name='detail'),

]
