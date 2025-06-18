from django import forms
from clients.models import Client, Contact

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['entity_name', 'contact', 'address', 'zip_code', 'city', 'phone_number', 'email']
        widgets = {
            'entity_name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'entity_name': 'Entité',
            'contact': 'Contact',
            'address': 'Adresse',
            'city': 'Ville',
            'zip_code': 'Code Postal',
            'phone_number': 'Téléphone',
            'email': 'Email',
        }
        # help_texts = {
        #     'email': 'Format: exemple@domaine.com',
        #     'phone_number': 'Format: 06 12 34 56 78',
        # }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['client', 'nom', 'prenom', 'fonction', 'phone_number', 'email', 'is_principal']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-input'}),
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'prenon': forms.TextInput(attrs={'class': 'form-input'}),
            'fonction': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'is_principal': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'client': 'Client',
            'nom': 'Nom',
            'prenon': 'Prénom',
            'fonction': 'Fonction',
            'phone_number': 'Téléphone',
            'email': 'Email',
            'is_principal': 'Contact principal',
        }