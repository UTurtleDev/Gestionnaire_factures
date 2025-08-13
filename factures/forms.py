from django import forms
from factures.models import Invoice, Payment
from users.models import CustomUser


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = CustomUser.objects.filter(is_author=True).order_by('first_name', 'last_name')
        
    class Meta:
        model = Invoice
        fields = ['date', 'type', 'affaire','invoice_number', 'client', 'contact', 'author', 'invoice_object', 'amount_ht', 'vat_rate']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'form-input'}),
            'affaire': forms.Select(attrs={'class': 'form-input'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-input'}),
            'client': forms.Select(attrs={'class': 'form-input'}),
            'contact': forms.Select(attrs={'class': 'form-input'}),
            'author': forms.Select(attrs={'class': 'form-input'}),
            'invoice_object': forms.Textarea(attrs={'class': 'form-area'}),
            'amount_ht': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'vat_rate': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }
        labels = {
            'date': 'Date',
            'type': 'Type',
            'affaire': 'Affaire',
            'invoice_number': 'N° Facture',
            'client': 'Client',
            'contact': 'Contact',
            'author': 'Auteur',
            'invoice_object': 'Description',
            'amount_ht': 'Montant HT',
            'vat_rate': 'Taux TVA'
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['date', 'amount', 'invoice', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'invoice': forms.Select(attrs={'class': 'form-input'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'date': 'Date',
            'amount': 'Montant',
            'invoice': 'N° Facture',
            'payment_method': 'Moyen de paiement',  
        }
