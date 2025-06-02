from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Donor, Recipient
from .forms import RecipientForm

@login_required
def main(request):
    donors = Donor.objects.all().order_by('-id')[:5]
    recipients = Recipient.objects.all().order_by('-id')[:5]

    context = {
        'donors': donors,
        'recipients': recipients
    }

    return render(request, 'main.html', context=context)

class DonorListView(LoginRequiredMixin, ListView):
    model = Donor
    template_name = 'donor_list.html'
    context_object_name = 'donors'
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        blood_group = self.request.GET.get('blood_group')
        national_code = self.request.GET.get('national_code')
        age = self.request.GET.get('age')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if national_code:
            queryset = queryset.filter(national_code=national_code)
        if age:
            queryset = queryset.filter(age=age)

        return queryset

class DonorCreateView(LoginRequiredMixin, CreateView):
    model = Donor
    fields = ['first_name', 'last_name', 'national_code', 'phone_number', 'age', 'blood_group', 'kdpi']
    template_name = 'donor_add.html'

    def get_success_url(self):
        return reverse('donor_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        blood_group = form.cleaned_data['blood_group']
        age = form.cleaned_data['age']
        kdpi = form.cleaned_data['kdpi']

        compatibility_map = {
            'A': ['A', 'AB'],
            'B': ['B', 'AB'],
            'AB': ['AB'],
            'O': ['O', 'A', 'B', 'AB'],
        }

        if kdpi <= 20:
            min_recipient_age = 0
            max_recipient_age = age
        elif 21 <= kdpi <= 75:
            if age < 25:
                min_recipient_age = 30
                max_recipient_age = 200
            else:
                min_recipient_age = age + 5
                max_recipient_age = 200
        else:
            min_recipient_age = age + 10
            max_recipient_age = 200

        form.instance.recipient_blood_group = compatibility_map.get(blood_group, [])
        form.instance.min_recipient_age = min_recipient_age
        form.instance.max_recipient_age = max_recipient_age

        return super().form_valid(form)

@login_required
def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)

    recipients = Recipient.objects.filter(
        Q(blood_group__in=donor.recipient_blood_group) &
        Q(age__gte=donor.min_recipient_age) & Q(age__lte=donor.max_recipient_age)
    ).order_by('-point')

    context = {
        'donor': donor,
        'recipients': recipients,
    }

    return render(request, 'donor_detail.html', context)

class DonorUpdateView(LoginRequiredMixin, UpdateView):
    model = Donor
    fields = ['first_name', 'last_name', 'national_code', 'phone_number', 'age', 'blood_group', 'kdpi']
    template_name = 'donor_form.html'

    def get_success_url(self):
        return reverse('donor_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        blood_group = form.cleaned_data['blood_group']
        age = form.cleaned_data['age']
        kdpi = form.cleaned_data['kdpi']

        compatibility_map = {
            'A': ['A', 'AB'],
            'B': ['B', 'AB'],
            'AB': ['AB'],
            'O': ['O', 'A', 'B', 'AB'],
        }

        if kdpi <= 20:
            min_recipient_age = 0
            max_recipient_age = age
        elif 21 <= kdpi <= 75:
            if age < 25:
                min_recipient_age = 30
                max_recipient_age = 200
            else:
                min_recipient_age = age + 5
                max_recipient_age = 200
        else:
            min_recipient_age = age + 10
            max_recipient_age = 200

        form.instance.recipient_blood_group = compatibility_map.get(blood_group, [])
        form.instance.min_recipient_age = min_recipient_age
        form.instance.max_recipient_age = max_recipient_age

        return super().form_valid(form)

class DonorDeleteView(LoginRequiredMixin, DeleteView):
    model = Donor
    template_name = 'donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        blood_group = self.request.GET.get('blood_group')
        national_code = self.request.GET.get('national_code')
        age = self.request.GET.get('age')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if national_code:
            queryset = queryset.filter(national_code=national_code)
        if age:
            queryset = queryset.filter(age=age)

        return queryset

class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_add.html'

    def get_success_url(self):
        return reverse('recipient_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        waiting_list = form.cleaned_data['waiting_list']
        dialysis_duration = form.cleaned_data['dialysis_duration']
        age = form.cleaned_data['age']
        previous_donation = form.cleaned_data['previous_donation']
        medical_urgency = form.cleaned_data['medical_urgency']
        candidate_for_2_kidney_TX = form.cleaned_data['candidate_for_2_kidney_TX']
        candidate_for_kidney_after_other_organ_TX = form.cleaned_data['candidate_for_kidney_after_other_organ_TX']
        cpra = form.cleaned_data['cpra']
        desensitized = form.cleaned_data['desensitized']
        hla = form.cleaned_data['hla_matching_and_mismatch_score']

        if 0 <= age <= 10:
            age_p = 4
        elif 11 <= age <= 17:
            age_p = 3
        else:
            age_p = 0
        
        if previous_donation == 'yes':
            previous_donation_p = 3
        else:
            previous_donation_p = 0
        
        if medical_urgency == '3':
            medical_urgency_p = 0
        else:
            medical_urgency_p = 3
        
        if candidate_for_2_kidney_TX == 'yes':
            candidate_for_2_kidney_TX_p = 2
        else:
            candidate_for_2_kidney_TX_p = 0

        if candidate_for_kidney_after_other_organ_TX == 'yes':
            candidate_for_kidney_after_other_organ_TX_p = 2
        else:
            candidate_for_kidney_after_other_organ_TX_p = 0

        if cpra == '1':
            cpra_p = 10
        elif cpra == '2':
            cpra_p = 4
        else:
            cpra_p = 0
        
        if desensitized == 'yes':
            desensitized_p = 10
        else:
            desensitized_p = 0

        point = waiting_list + (dialysis_duration * 0.5) + age_p + previous_donation_p + medical_urgency_p + candidate_for_2_kidney_TX_p + candidate_for_kidney_after_other_organ_TX_p + cpra_p + desensitized_p + hla

        form.instance.point = point

        return super().form_valid(form)

@login_required
def recipient_detail(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)

    dialysis_duration_p = (recipient.dialysis_duration) * 0.5
    age = recipient.age
    previous_donation = recipient.previous_donation
    medical_urgency = recipient.medical_urgency
    candidate_for_2_kidney_TX = recipient.candidate_for_2_kidney_TX
    candidate_for_kidney_after_other_organ_TX = recipient.candidate_for_kidney_after_other_organ_TX
    cpra = recipient.cpra
    desensitized = recipient.desensitized

    if 0 <= age <= 10:
        age_p = 4
    elif 11 <= age <= 17:
        age_p = 3
    else:
        age_p = 0
        
    if previous_donation == 'yes':
        previous_donation_p = 3
    else:
        previous_donation_p = 0
    
    if medical_urgency == '3':
        medical_urgency_p = 0
    else:
        medical_urgency_p = 3
        
    if candidate_for_2_kidney_TX == 'yes':
        candidate_for_2_kidney_TX_p = 2
    else:
        candidate_for_2_kidney_TX_p = 0

    if candidate_for_kidney_after_other_organ_TX == 'yes':
        candidate_for_kidney_after_other_organ_TX_p = 2
    else:
        candidate_for_kidney_after_other_organ_TX_p = 0

    if cpra == '1':
        cpra_p = 10
    elif cpra == '2':
        cpra_p = 4
    else:
        cpra_p = 0

    if desensitized == 'yes':
        desensitized_p = 10
    else:
        desensitized_p = 0

    context = {
        'recipient': recipient,
        'dialysis_duration_p': dialysis_duration_p,
        'age_p': age_p,
        'previous_donation_p': previous_donation_p,
        'medical_urgency_p': medical_urgency_p,
        'candidate_for_2_kidney_TX_p': candidate_for_2_kidney_TX_p,
        'candidate_for_kidney_after_other_organ_TX_p': candidate_for_kidney_after_other_organ_TX_p,
        'cpra_p': cpra_p,
        'desensitized_p': desensitized_p,
    }

    return render(request, 'recipient_detail.html', context)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'

    def get_success_url(self):
        return reverse('recipient_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        waiting_list = form.cleaned_data['waiting_list']
        dialysis_duration = form.cleaned_data['dialysis_duration']
        age = form.cleaned_data['age']
        previous_donation = form.cleaned_data['previous_donation']
        medical_urgency = form.cleaned_data['medical_urgency']
        candidate_for_2_kidney_TX = form.cleaned_data['candidate_for_2_kidney_TX']
        candidate_for_kidney_after_other_organ_TX = form.cleaned_data['candidate_for_kidney_after_other_organ_TX']
        cpra = form.cleaned_data['cpra']
        desensitized = form.cleaned_data['desensitized']
        hla = form.cleaned_data['hla_matching_and_mismatch_score']

        if 0 <= age <= 10:
            age_p = 4
        elif 11 <= age <= 17:
            age_p = 3
        else:
            age_p = 0
        
        if previous_donation == 'yes':
            previous_donation_p = 3
        else:
            previous_donation_p = 0
        
        if medical_urgency == '3':
            medical_urgency_p = 0
        else:
            medical_urgency_p = 3
        
        if candidate_for_2_kidney_TX == 'yes':
            candidate_for_2_kidney_TX_p = 2
        else:
            candidate_for_2_kidney_TX_p = 0

        if candidate_for_kidney_after_other_organ_TX == 'yes':
            candidate_for_kidney_after_other_organ_TX_p = 2
        else:
            candidate_for_kidney_after_other_organ_TX_p = 0

        if cpra == '1':
            cpra_p = 10
        elif cpra == '2':
            cpra_p = 4
        else:
            cpra_p = 0
        
        if desensitized == 'yes':
            desensitized_p = 10
        else:
            desensitized_p = 0

        point = waiting_list + (dialysis_duration * 0.5) + age_p + previous_donation_p + medical_urgency_p + candidate_for_2_kidney_TX_p + candidate_for_kidney_after_other_organ_TX_p + cpra_p + desensitized_p + hla

        form.instance.point = point

        return super().form_valid(form)

class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')
