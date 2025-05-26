from django import forms
from .models import Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['point']