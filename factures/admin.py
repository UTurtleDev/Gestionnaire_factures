from django.contrib import admin
from .models import Invoice, Payment
from datetime import datetime

# Register your models here.

# Filtres intelligents dans l'interface admin
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'get_client_name', 'formatted_amount_ht', 'formatted_amount_ttc', 'statut', 'day_late')
    list_filter = ('date', 'statut')
    search_fields = ('invoice_number', 'client_entity_name', 'client__entity_name')

    def day_late(self, obj):
        if obj.statut == 'en_retard':
            return (datetime.today().date() - obj.due_date).days
        return 0
    
    day_late.short_description = 'Jours en retard'

    
    def get_client_name(self, obj):
        if obj.client:
            return obj.client.entity_name
        return obj.client_entity_name
    
    get_client_name.short_description = 'Client'

    # Cette méthode s'assure que client_entity_name est rempli dans l'admin
    def save_model(self, request, obj, form, change):
        # Si le client existe, copie son nom dans client_entity_name
        if obj.client:
            obj.client_entity_name = obj.client.entity_name
        super().save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)
