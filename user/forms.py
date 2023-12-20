from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                        'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                        'dark:placeholder-gray-400 dark:text-white '
                                                        'dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                            'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                            'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                            'dark:placeholder-gray-400 dark:text-white '
                                                            'dark:focus:ring-blue-500 dark:focus:border-blue-500'})


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
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
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                         'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                         'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                         'dark:placeholder-gray-400 dark:text-white '
                                                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                                                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                        'p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                                                        'dark:placeholder-gray-400 dark:text-white '
                                                        'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        }