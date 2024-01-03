from django import forms


class DataForm(forms.Form):
    file = forms.FileField()
