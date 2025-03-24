from django import forms
from factures.models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'type', 'affaire','invoice_number', 'client_entity_name', 'objet', 'amount_ht', 'value_rate']
        widgets = {
            # 'date': forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-date'})),
            'date': forms.TextInput(attrs={'class': 'form-input'}),
            'type': forms.TextInput(attrs={'class': 'form-input'}),
            'affaire': forms.TextInput(attrs={'class': 'form-input'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-input'}),
            'client_entity_name': forms.TextInput(attrs={'class': 'form-input'}),
            'objet': forms.TextInput(attrs={'class': 'form-input'}),
            'amount_ht': forms.TextInput(attrs={'class': 'form-input'}),
            'value_rate': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'date': 'Date',
            'type': 'Type',
            'affaire': 'Affaire',
            'invoice_number': 'N° Facture',
            'client_entity_name': 'Client',
            'objet': 'Description',
            'amount_ht': 'Montant HT',
            'value_rate': 'Taux TVA'
        }
