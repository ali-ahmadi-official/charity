from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from .models import CadaverDonor, LivingDonor, Recipient, DonorTest, RecipientTest, HistoryCall

CustomUser = get_user_model()

class CustomLoginForm(AuthenticationForm):
    captcha = CaptchaField(label='کد امنیتی')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='نام', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_superuser = forms.BooleanField(label='دسترسی پزشک', required=False)
    is_staff = forms.BooleanField(label='اکانت تستی', required=False)
    groups = forms.ModelMultipleChoiceField(label="کلینیک‌ها", queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'is_staff', 'groups',)

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'groups')
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'groups': 'کلینیک ها',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple,
        }

class CadaverDonorForm(forms.ModelForm):
    class Meta:
        model = CadaverDonor
        exclude = ['recipient_blood_group', 'min_recipient_age', 'max_recipient_age', 'status', 'is_test', 'creator_user', 'creator_groups']

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
        exclude = ['recipient_blood_group', 'min_recipient_age', 'max_recipient_age', 'status', 'is_test', 'creator_user', 'creator_groups']

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
        exclude = ['point', 'donor_blood_group', 'min_donor_age', 'max_donor_age', 'is_test', 'creator_user', 'creator_groups']

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

            'hla_a_uam': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_b_uam': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb1_uam': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb_uam': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_dqb1_uam': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
        }

class DonorTestForm(forms.ModelForm):
    class Meta:
        model = DonorTest
        exclude = ['is_test', 'creator_user', 'creator_groups']

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
        exclude = ['is_test', 'creator_user', 'creator_groups']

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

class HistoryCallForm(forms.ModelForm):
    class Meta:
        model = HistoryCall
        exclude = ['recipient']

        widgets = {
            'hla_a_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_b_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb1_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_dqb1_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
        }

class HistoryCallUpdateForm(forms.ModelForm):
    class Meta:
        model = HistoryCall
        exclude = ['recipient', 'class_i_pdf', 'class_ii_pdf']

        widgets = {
            'hla_a_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_b_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb1_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_drb_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
            'hla_dqb1_uam_history': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple uam_multi'}),
        }

class AddGroupToDonorsForm(forms.Form):
    living_donors = forms.ModelMultipleChoiceField(
        queryset=LivingDonor.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"}),
        label="اهداکنندگان living",
    )

    cadaver_donors = forms.ModelMultipleChoiceField(
        queryset=CadaverDonor.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"}),
        label="اهداکنندگان cadaver",
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        widget=forms.Select(attrs={"class": "form-control select2"}),
        label="کلینیک مقصد",
        empty_label="انتخاب کلینیک",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        user_groups = user.groups.all()

        self.fields["group"].queryset = Group.objects.exclude(
            id__in=user_groups.values("id")
        )

        if user.id == 1:
            self.fields["living_donors"].queryset = LivingDonor.objects.all()
        elif user_groups.exists():
            self.fields["living_donors"].queryset = LivingDonor.objects.filter(
                creator_groups__in=user_groups
            ).distinct()

        if user.id == 1:
            self.fields["cadaver_donors"].queryset = CadaverDonor.objects.all()
        elif user_groups.exists():
            self.fields["cadaver_donors"].queryset = CadaverDonor.objects.filter(
                creator_groups__in=user_groups
            ).distinct()

class AddGroupToRecipientsForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"}),
        label="گیرندگان",
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        widget=forms.Select(attrs={"class": "form-control select2"}),
        label="کلینیک مقصد",
        empty_label="انتخاب کلینیک",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        user_groups = user.groups.all()

        self.fields["group"].queryset = Group.objects.exclude(
            id__in=user_groups.values("id")
        )

        if user.id == 1:
            self.fields["recipients"].queryset = Recipient.objects.all()
        elif user_groups.exists():
            self.fields["recipients"].queryset = Recipient.objects.filter(
                creator_groups__in=user_groups
            ).distinct()
            