from django import forms
from factures.models import Invoice, Payment
from users.models import CustomUser


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = CustomUser.objects.filter(is_author=True).order_by('first_name', 'last_name')
    
    def clean(self):
        """Validation automatique des montants pour les avoirs"""
        cleaned_data = super().clean()
        type_facture = cleaned_data.get('type')
        amount_ht = cleaned_data.get('amount_ht')
        
        # Si c'est un avoir et que le montant est positif, le convertir en négatif
        if type_facture == 'avoir' and amount_ht and amount_ht > 0:
            cleaned_data['amount_ht'] = -amount_ht
            
        return cleaned_data
        
    class Meta:
        model = Invoice
        fields = ['date', 'type', 'affaire','invoice_number', 'client', 'contact', 'author', 'invoice_object', 'amount_ht', 'vat_rate', 'facture_pdf']
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
            'facture_pdf': forms.FileInput(attrs={'class': 'form-input', 'accept': '.pdf'}),
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
            'vat_rate': 'Taux TVA',
            'facture_pdf': 'Facture PDF'
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
