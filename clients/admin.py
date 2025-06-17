from django.contrib import admin
from .models import Client, Contact

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'client','fonction', 'phone_number', 'email', 'is_principal')

admin.site.register(Client)
admin.site.register(Contact, ClientAdmin)

    