from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django import forms
from .models import CustomUser


class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(), label='IIN:')
    password = forms.CharField(widget=forms.PasswordInput())


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('iin', 'phone', 'birth_date')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('iin', 'phone', 'birth_date', 'surname', 'name', 'patronymic', 'photo',
                  'is_staff', 'is_superuser', 'is_active', 'group')

    def clean_password(self):
        return self.initial["password"]
