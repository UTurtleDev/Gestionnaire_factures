from django import forms
from django.forms import formset_factory, inlineformset_factory
from clients.models import Client, Contact

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['entity_name', 'address', 'zip_code', 'city', 'phone_number', 'email']
        widgets = {
            'entity_name': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'entity_name': 'Entité',
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
            'prenom': forms.TextInput(attrs={'class': 'form-input'}),
            'fonction': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'is_principal': forms.CheckboxInput(attrs={'class': 'form-checkbox principal-checkbox'}),
        }
        labels = {
            'client': 'Client',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'fonction': 'Fonction',
            'phone_number': 'Téléphone',
            'email': 'Email',
            'is_principal': 'Contact principal',
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Check if at least one field is filled
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom') 
        fonction = cleaned_data.get('fonction')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        
        # If all fields are empty, this form should be considered empty
        if not any([nom, prenom, fonction, phone_number, email]):
            # Mark this form as empty - Django formsets will ignore empty forms
            self._is_empty_form = True
        else:
            # If form has data, require at least nom or prenom
            if not nom and not prenom:
                raise forms.ValidationError("Au moins un nom ou prénom est requis pour un contact.")
        
        return cleaned_data
    
    def has_changed(self):
        """Override to properly detect if form has changed"""
        if hasattr(self, '_is_empty_form'):
            return False
        return super().has_changed()

class BaseContactFormSet(forms.BaseFormSet):
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
        
        # Ensure we have at least one contact
        if not valid_forms:
            raise forms.ValidationError("Au moins un contact est requis.")
        
        # Ensure exactly one principal contact
        if principal_count == 0:
            # Automatically make the first contact principal
            if valid_forms:
                valid_forms[0].cleaned_data['is_principal'] = True
        elif principal_count > 1:
            raise forms.ValidationError("Un seul contact peut être marqué comme principal.")

# Create the ContactFormSet
ContactFormSet = formset_factory(
    ContactForm,
    formset=BaseContactFormSet,
    extra=1,  # Start with 1 empty form
    min_num=1,  # Require at least 1 contact
    max_num=10,  # Limit to 10 contacts max
    validate_min=True,
    can_delete=True
)

# Create ContactInlineFormSet for client updates
ContactInlineFormSet = inlineformset_factory(
    Client, 
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