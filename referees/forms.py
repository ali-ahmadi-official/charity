from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CadaverDonor, LivingDonor, Recipient, DonorTest, RecipientTest

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class CadaverDonorForm(forms.ModelForm):
    class Meta:
        model = CadaverDonor
        exclude = ['recipient_blood_group', 'min_recipient_age', 'max_recipient_age', 'status']

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

class LivingDonorForm(forms.ModelForm):
    class Meta:
        model = LivingDonor
        exclude = ['recipient_blood_group', 'min_recipient_age', 'max_recipient_age', 'status']

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
        exclude = ['point', 'donor_blood_group', 'min_donor_age', 'max_donor_age']

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