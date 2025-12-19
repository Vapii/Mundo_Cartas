from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Correo electrónico...",
            "class": "input-registro"
        })
    )

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "username...",
                "class": "input-registro"
            }),
            "password1": forms.PasswordInput(attrs={
                "placeholder": "Password...",
                "class": "input-registro"
            }),
            "password2": forms.PasswordInput(attrs={
                "placeholder": "Password...",
                "class": "input-registro"
            }),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'placeholder': 'user...',
            'class': 'input-login'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password...',
            'class': 'input-login'
        })
    )
