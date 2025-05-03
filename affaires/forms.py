from django import forms
from affaires.models import Affaire

class AffaireForm(forms.ModelForm):
    class Meta:
        model = Affaire
        fields = ['affaire_number', 'client', 'budget', 'affaire_description']
        widgets = {
            'affaire_number': forms.TextInput(attrs={'class': 'form-input'}),
            'client': forms.Select(attrs={'class': 'form-input'}),
            'budget': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'affaire_description': forms.Textarea(attrs={'class': 'form-area'}),
        }
        labels = {
            'affaire_number': "N° d'affaire",
            'client': 'Client',
            'budget': "Budget",
            'affaire_description': "Objet",
        }