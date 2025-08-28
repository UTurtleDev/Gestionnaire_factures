from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label='Mot de passe',
        # help_text='Laissez vide pour ne pas modifier le mot de passe lors d\'une modification.'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label='Confirmer le mot de passe'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_author']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_author': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'email': 'Email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'is_active': 'Utilisateur actif',
            'is_staff': 'Administrateur',
            'is_author': 'Auteur',
        }

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)
        
        if self.is_update:
            # Pour la modification, le mot de passe n'est pas obligatoire
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = 'Laissez vide pour ne pas modifier le mot de passe.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Vérifier que l'email n'existe pas déjà pour un autre utilisateur
            existing_user = User.objects.filter(email=email).first()
            if existing_user and (not self.instance or existing_user.pk != self.instance.pk):
                raise forms.ValidationError("Un utilisateur avec cette adresse email existe déjà.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Validation du mot de passe seulement si c'est une création ou si le mot de passe est fourni
        if not self.is_update or password:
            if not password:
                raise forms.ValidationError("Le mot de passe est requis.")
            
            if password != confirm_password:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
            
            if len(password) < 6:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 6 caractères.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user


class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        kwargs['is_update'] = True
        super().__init__(*args, **kwargs)
        
        # Les champs de mot de passe sont optionnels pour la modification
        if 'password' in self.fields:
            self.fields['password'].help_text = 'Laissez vide pour ne pas modifier le mot de passe.'
        if 'confirm_password' in self.fields:
            self.fields['confirm_password'].help_text = 'Confirmer le nouveau mot de passe.'


class UserCreateForm(UserForm):
    def __init__(self, *args, **kwargs):
        kwargs['is_update'] = False
        super().__init__(*args, **kwargs)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'signin_input',
            'placeholder': 'Email'
        }),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'signin_input', 
            'placeholder': 'Password'
        }),
        label=''
    )
    
    error_messages = {
        'invalid_login': 'Email ou mot de passe incorrect.',
        'inactive': 'Ce compte est inactif.',
    }