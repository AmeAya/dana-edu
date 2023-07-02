from django.contrib.auth.forms import AuthenticationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(), label='IIN:')
    password = forms.CharField(widget=forms.PasswordInput())
