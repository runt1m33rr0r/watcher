from django import forms
from django.forms import ModelForm
from .models import Settings


class AddPersonForm(forms.Form):
    name = forms.CharField(max_length=50)
    image = forms.ImageField()


class UploadImageForm(forms.Form):
    image = forms.ImageField()


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'