from django import forms


class AttachedFile(forms.Form):
    data_form = forms.FileField()