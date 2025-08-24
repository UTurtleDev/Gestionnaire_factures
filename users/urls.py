
from django.urls import path
from .views import users, user_create, user_detail, user_update, user_delete

app_name = 'users'

urlpatterns = [
    path('', users , name="users"),
    path('nouveau/', user_create , name="create"),
    path('<int:pk>/modifier/', user_update , name="modifier"),
    path('<int:pk>', user_detail , name="detail"),
    path('<int:pk>/supprimer/', user_delete , name="delete"),
]
