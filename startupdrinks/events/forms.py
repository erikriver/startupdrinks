from django import forms
from django.utils.translation import gettext as _
from .models import KIND_CHOICES

class UserForm(forms.Form):
    """
    """
    fullname = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    kind = forms.ChoiceField(widget=forms.Select, choices=KIND_CHOICES)
    bio = forms.CharField(widget=forms.Textarea, required=True)
    expect = forms.CharField(widget=forms.Textarea, required=True)
        
