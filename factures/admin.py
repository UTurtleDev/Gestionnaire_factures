from django.contrib import admin
from .models import Invoice, Payment

# Register your models here.

# Filtres intelligents dans l'interface admin
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'client', 'amount_ht', 'amount_ttc', 'statut', 'day_late')
    list_filter = ('date', 'client', 'statut')
    search_fields = ('invoice_number', 'client__company', 'client__entity_name')

    def day_late(self, obj):
        if obj.statut == 'en_retard':
            return (obj.due_date - obj.date).days
        return 0
    
    day_late.short_description = 'Jours en retard'

    


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)