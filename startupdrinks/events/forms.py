from django import forms
from django.utils.translation import gettext as _

class UserForm(forms.Form):
    """
    """
    fullname = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=True)
        