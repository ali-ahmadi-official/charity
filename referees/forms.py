from django import forms
from .models import Donor, Recipient, DonorTest, RecipientTest

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ['recipient_blood_group', 'min_recipient_age', 'max_recipient_age']

        widgets = {
            'hla_a_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_a_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_2': forms.Select(attrs={'class': 'form-control'}),
        }

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['point']

        widgets = {
            'hla_a_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_a_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_2': forms.Select(attrs={'class': 'form-control'}),
        }

class DonorTestForm(forms.ModelForm):
    class Meta:
        model = DonorTest
        fields = '__all__'

        widgets = {
            'hla_a_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_a_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_2': forms.Select(attrs={'class': 'form-control'}),
        }

class RecipientTestForm(forms.ModelForm):
    class Meta:
        model = RecipientTest
        fields = '__all__'

        widgets = {
            'hla_a_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_a_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_b_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb1_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_drb_2': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_1': forms.Select(attrs={'class': 'form-control'}),
            'hla_dqb1_2': forms.Select(attrs={'class': 'form-control'}),
        }