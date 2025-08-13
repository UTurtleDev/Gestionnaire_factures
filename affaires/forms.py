from django import forms
from affaires.models import Affaire
from users.models import CustomUser

class AffaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = CustomUser.objects.filter(is_author=True).order_by('first_name', 'last_name')
        
    class Meta:
        model = Affaire
        fields = ['affaire_number', 'client', 'author', 'budget', 'affaire_description']
        widgets = {
            'affaire_number': forms.TextInput(attrs={'class': 'form-input'}),
            'client': forms.Select(attrs={'class': 'form-input'}),
            'author': forms.Select(attrs={'class': 'form-input'}),
            'budget': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'affaire_description': forms.Textarea(attrs={'class': 'form-area'}),
        }
        labels = {
            'affaire_number': "N° d'affaire",
            'client': 'Client',
            'author': 'Auteur',
            'budget': "Budget",
            'affaire_description': "Objet",
        }