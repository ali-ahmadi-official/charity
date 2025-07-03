from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Donor, Recipient, HlaA, HlaB, HlaDRB1, HlaDRB, HlaDQB1
from .forms import DonorForm, RecipientForm
from .jalali import Persian

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
    form_class = DonorForm
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
    form_class = DonorForm
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

        if isinstance(waiting_list, str):
            try:
                waiting_list_date = Persian(waiting_list).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - waiting_list_date).days
                waiting_list_p = round((delta_days / 365), 2)
            except:
                pass
        
        if isinstance(dialysis_duration, str):
            try:
                dialysis_duration_date = Persian(dialysis_duration).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - dialysis_duration_date).days
                dialysis_duration_p = (delta_days / 365)
            except:
                pass

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

        point = waiting_list_p + round((dialysis_duration_p * 0.5), 2) + age_p + previous_donation_p + medical_urgency_p + candidate_for_2_kidney_TX_p + candidate_for_kidney_after_other_organ_TX_p + cpra_p + desensitized_p

        form.instance.point = point

        return super().form_valid(form)

@login_required
def recipient_detail(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)

    if isinstance(recipient.waiting_list, str):
        try:
            waiting_list_date = Persian(recipient.waiting_list).gregorian_datetime()
            now_date = datetime.now().date()
            delta_days = (now_date - waiting_list_date).days
            waiting_list_p = round((delta_days / 365), 2)
        except:
            pass
        
    if isinstance(recipient.dialysis_duration, str):
        try:
            dialysis_duration_date = Persian(recipient.dialysis_duration).gregorian_datetime()
            now_date = datetime.now().date()
            delta_days = (now_date - dialysis_duration_date).days
            dialysis_duration_p = (delta_days / 365)
        except:
            pass

    dialysis_duration_p = round((dialysis_duration_p * 0.5), 2)
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
        'waiting_list_p': waiting_list_p,
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

        if isinstance(waiting_list, str):
            try:
                waiting_list_date = Persian(waiting_list).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - waiting_list_date).days
                waiting_list_p = round((delta_days / 365), 2)
            except:
                pass
        
        if isinstance(dialysis_duration, str):
            try:
                dialysis_duration_date = Persian(dialysis_duration).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - dialysis_duration_date).days
                dialysis_duration_p = (delta_days / 365)
            except:
                pass

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

        point = waiting_list_p + round((dialysis_duration_p * 0.5), 2) + age_p + previous_donation_p + medical_urgency_p + candidate_for_2_kidney_TX_p + candidate_for_kidney_after_other_organ_TX_p + cpra_p + desensitized_p

        form.instance.point = point

        return super().form_valid(form)

class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')

@login_required
def hla_lists(request):
    hla_as = HlaA.objects.all()
    hla_bs = HlaB.objects.all()
    hla_drb1s = HlaDRB1.objects.all()
    hla_drbs = HlaDRB.objects.all()
    hla_dqb1s = HlaDQB1.objects.all()

    context = {
        'hla_as': hla_as,
        'hla_bs': hla_bs,
        'hla_drb1s': hla_drb1s,
        'hla_drbs': hla_drbs,
        'hla_dqb1s': hla_dqb1s,
    }

    return render(request, 'hla/hla_lists.html', context=context)

class HlaACreateview(LoginRequiredMixin, CreateView):
    model = HlaA
    fields = '__all__'
    template_name = 'hla/hla_a_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaAUpdateView(LoginRequiredMixin, UpdateView):
    model = HlaA
    fields = '__all__'
    template_name = 'hla/hla_a_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaADeleteView(LoginRequiredMixin, DeleteView):
    model = HlaA
    template_name = 'hla/hla_a_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaBCreateview(LoginRequiredMixin, CreateView):
    model = HlaB
    fields = '__all__'
    template_name = 'hla/hla_b_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaBUpdateView(LoginRequiredMixin, UpdateView):
    model = HlaB
    fields = '__all__'
    template_name = 'hla/hla_b_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaBDeleteView(LoginRequiredMixin, DeleteView):
    model = HlaB
    template_name = 'hla/hla_b_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDRB1Createview(LoginRequiredMixin, CreateView):
    model = HlaDRB1
    fields = '__all__'
    template_name = 'hla/hla_drb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRB1UpdateView(LoginRequiredMixin, UpdateView):
    model = HlaDRB1
    fields = '__all__'
    template_name = 'hla/hla_drb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRB1DeleteView(LoginRequiredMixin, DeleteView):
    model = HlaDRB1
    template_name = 'hla/hla_drb1_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDRBCreateview(LoginRequiredMixin, CreateView):
    model = HlaDRB
    fields = '__all__'
    template_name = 'hla/hla_drb_form.html'

    def get_success_url(self):
        return reverse('hla_lists')
    
class HlaDRBUpdateView(LoginRequiredMixin, UpdateView):
    model = HlaDRB
    fields = '__all__'
    template_name = 'hla/hla_drb_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRBDeleteView(LoginRequiredMixin, DeleteView):
    model = HlaDRB
    template_name = 'hla/hla_drb_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDQB1Createview(LoginRequiredMixin, CreateView):
    model = HlaDQB1
    fields = '__all__'
    template_name = 'hla/hla_dqb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDQB1UpdateView(LoginRequiredMixin, UpdateView):
    model = HlaDQB1
    fields = '__all__'
    template_name = 'hla/hla_dqb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDQB1DeleteView(LoginRequiredMixin, DeleteView):
    model = HlaDQB1
    template_name = 'hla/hla_dqb1_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

@login_required
def auto_add_hla(request):
    hla_a_choices = [
        ('A*01', '1'), ('A*02', '1'), ('A*03', '1'), ('A*07', '3'),
        ('A*10', '2'), ('A*11', '1'), ('A*12', '3'), ('A*23', '3'),
        ('A*24', '1'), ('A*25', '3'), ('A*26', '2'), ('A*28', '2'),
        ('A*29', '3'), ('A*30', '3'), ('A*31', '3'), ('A*32', '2'),
        ('A*33', '3'), ('A*34', '3'), ('A*36', '3'), ('A*43', '3'),
        ('A*66', '3'), ('A*68', '2'), ('A*69', '3'), ('A*74', '3'),
        ('A*80', '3'),
    ]

    hla_b_choices = [
        ('B*05', '1'), ('B*07', '2'), ('B*08', '3'), ('B*13', '2'),
        ('B*14', '3'), ('B*15', '2'), ('B*18', '2'), ('B*21', '3'),
        ('B*22', '3'), ('B*27', '3'), ('B*35', '1'), ('B*37', '3'),
        ('B*38', '2'), ('B*39', '3'), ('B*40', '3'), ('B*41', '3'),
        ('B*42', '3'), ('B*44', '2'), ('B*45', '3'), ('B*46', '3'),
        ('B*47', '3'), ('B*48', '3'), ('B*49', '3'), ('B*50', '2'),
        ('B*51', '1'), ('B*52', '3'), ('B*53', '3'), ('B*54', '3'),
        ('B*55', '3'), ('B*56', '3'), ('B*57', '3'), ('B*58', '3'),
        ('B*73', '3'), ('B*78', '3'), ('B*81', '3'),
    ]

    hla_drb1_choices = [
        ('DRB1*01', '2'), ('DRB1*03', '1'), ('DRB1*04', '1'), ('DRB1*07', '1'),
        ('DRB1*08', '3'), ('DRB1*09', '3'), ('DRB1*10', '3'), ('DRB1*11', '1'),
        ('DRB1*12', '3'), ('DRB1*13', '1'), ('DRB1*14', '2'), ('DRB1*15', '1'),
        ('DRB1*16', '2'),
    ]

    hla_dqb1_choices = [
        ('DQB1*02', '1'), ('DQB1*03', '1'), ('DQB1*04', '2'), ('DQB1*05', '1'), ('DQB1*06', '1'),
    ]

    for value, type_ in hla_a_choices:
        HlaA.objects.create(value=value, type=type_)

    for value, type_ in hla_b_choices:
        HlaB.objects.create(value=value, type=type_)

    for value, type_ in hla_drb1_choices:
        HlaDRB1.objects.create(value=value, type=type_)

    for value, type_ in hla_dqb1_choices:
        HlaDQB1.objects.create(value=value, type=type_)

    return redirect('main')