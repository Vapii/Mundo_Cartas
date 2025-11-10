from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico...',
            'class': 'input-registro'
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'input-file'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'correo', 'avatar', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'username...',
                'class': 'input-registro'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password...',
                'class': 'input-registro'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Password...',
                'class': 'input-registro'
            }),
        }

    
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
