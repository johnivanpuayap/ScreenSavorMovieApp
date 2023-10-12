from django.forms import ModelForm
from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg '
                                               'focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                                               'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                                               'dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                   'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                   'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                   'dark:placeholder-gray-400 dark:text-white '
                                                   'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
    )


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'firstname', 'lastname']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                        'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                        'dark:placeholder-gray-400 dark:text-white '
                                                        'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'password': forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                            'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                            'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                            'dark:placeholder-gray-400 dark:text-white '
                                                            'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'firstname': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                         'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                         'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                         'dark:placeholder-gray-400 dark:text-white '
                                                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'lastname': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                        'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                        'dark:placeholder-gray-400 dark:text-white '
                                                        'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        }
