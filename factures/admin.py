from django.contrib import admin
from .models import Invoice, Payment
from datetime import datetime

# Register your models here.

# Filtres intelligents dans l'interface admin
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'client', 'formatted_amount_ht', 'formatted_amount_ttc', 'statut', 'day_late')
    list_filter = ('date', 'client', 'statut')
    search_fields = ('invoice_number', 'client__company', 'client__entity_name')

    def day_late(self, obj):
        if obj.statut == 'en_retard':
            return (datetime.today().date() - obj.due_date).days
        return 0
    
    day_late.short_description = 'Jours en retard'

    


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)
