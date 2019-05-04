from django import forms

class AddPersonForm(forms.Form):
    name = forms.CharField(max_length=50)
    image = forms.ImageField()
