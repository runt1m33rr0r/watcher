from django import forms
from django.forms import ModelForm
from .models import Settings, Detection


class AddPersonForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=50)
    image = forms.ImageField()


class UploadImageForm(forms.Form):
    image = forms.ImageField()


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'


class UsernameForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=20)


class PasswordForm(forms.Form):
    password = forms.CharField(min_length=8, max_length=50)


class AlertForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=50)
    city = forms.CharField(min_length=2, max_length=50)
    image = forms.ImageField()