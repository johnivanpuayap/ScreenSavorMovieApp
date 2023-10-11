from django.forms import ModelForm
from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'johndoe123'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'max of 32 characters'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'John'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Doe'}),
        }


