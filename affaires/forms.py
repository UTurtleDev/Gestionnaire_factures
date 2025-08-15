from django import forms
from django.forms import formset_factory, inlineformset_factory
from affaires.models import Affaire
from users.models import CustomUser
from clients.models import Contact
from clients.forms import ContactForm

class AffaireForm(forms.ModelForm):
    existing_contact = forms.ModelChoiceField(
        queryset=Contact.objects.none(),
        empty_label="Sélectionner un contact existant",
        required=False,
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'existing-contact-select'}),
        label="Contact existant"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = CustomUser.objects.filter(is_author=True).order_by('first_name', 'last_name')
        
        # If we have a client selected, populate existing contacts
        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['existing_contact'].queryset = Contact.objects.filter(
                    affaire__client_id=client_id
                ).distinct().order_by('nom', 'prenom')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.client:
            # For updates, show contacts from the same client
            self.fields['existing_contact'].queryset = Contact.objects.filter(
                affaire__client=self.instance.client
            ).distinct().order_by('nom', 'prenom')
        
    class Meta:
        model = Affaire
        fields = ['affaire_number', 'client', 'author', 'budget', 'affaire_description']
        widgets = {
            'affaire_number': forms.TextInput(attrs={'class': 'form-input'}),
            'client': forms.Select(attrs={'class': 'form-input', 'id': 'client-select'}),
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



class BaseContactFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.existing_contact_selected = kwargs.pop('existing_contact_selected', False)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """Validates that at least one contact exists and exactly one is principal"""
        if any(self.errors):
            # Don't validate if individual forms have errors
            return
        
        valid_forms = []
        principal_count = 0
        
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            
            # Skip empty forms
            if hasattr(form, '_is_empty_form') and form._is_empty_form:
                continue
                
            if form.cleaned_data:
                valid_forms.append(form)
                if form.cleaned_data.get('is_principal'):
                    principal_count += 1
        
        # If an existing contact is selected, we don't require new contacts from formset
        if not self.existing_contact_selected and not valid_forms:
            raise forms.ValidationError("Au moins un contact est requis.")
        
        # Ensure exactly one principal contact (but only if we have new contacts or no existing contact selected)
        if valid_forms:
            if principal_count == 0:
                # Automatically make the first contact principal only if no existing contact is selected
                if not self.existing_contact_selected:
                    valid_forms[0].cleaned_data['is_principal'] = True
            elif principal_count > 1:
                raise forms.ValidationError("Un seul contact peut être marqué comme principal.")


# Create the ContactFormSet for affaire creation
ContactFormSet = formset_factory(
    ContactForm,
    formset=BaseContactFormSet,
    extra=1,  # Start with 1 empty form
    min_num=1,  # Require at least 1 contact
    max_num=10,  # Limit to 10 contacts max
    validate_min=True,
    can_delete=True
)

# Create ContactInlineFormSet for affaire updates
ContactInlineFormSet = inlineformset_factory(
    Affaire, 
    Contact,
    fields=['nom', 'prenom', 'fonction', 'phone_number', 'email', 'is_principal'],
    widgets={
        'nom': forms.TextInput(attrs={'class': 'form-input'}),
        'prenom': forms.TextInput(attrs={'class': 'form-input'}),
        'fonction': forms.TextInput(attrs={'class': 'form-input'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
        'email': forms.EmailInput(attrs={'class': 'form-input'}),
        'is_principal': forms.CheckboxInput(attrs={'class': 'form-checkbox principal-checkbox'}),
    },
    labels={
        'nom': 'Nom',
        'prenom': 'Prénom', 
        'fonction': 'Fonction',
        'phone_number': 'Téléphone',
        'email': 'Email',
        'is_principal': 'Contact principal',
    },
    extra=0,  # Don't show extra empty forms by default
    min_num=1,  # Require at least 1 contact
    max_num=10,  # Limit to 10 contacts max
    validate_min=True,
    can_delete=True
)