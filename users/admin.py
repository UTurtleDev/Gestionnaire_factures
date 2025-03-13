from django.contrib import admin
from .models import CustomUser

# Register your models here.

class usersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email' 'is_active', 'is_staff')

admin.site.register(CustomUser)