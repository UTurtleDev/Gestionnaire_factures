from django.contrib import admin
from .models import Affaire

# Register your models here.

class AffaireAdmin(admin.ModelAdmin):
    list_display = ('affaire_number', 'affaire_description', 'client', 'budget')

admin.site.register(Affaire, AffaireAdmin)