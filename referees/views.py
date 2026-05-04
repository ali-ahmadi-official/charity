from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import CadaverDonor, LivingDonor, Recipient, HlaA, HlaB, HlaDRB1, HlaDRB, HlaDQB1, DonorTest, RecipientTest
from .forms import CustomUserCreationForm, CustomUserChangeForm, CadaverDonorForm, LivingDonorForm, RecipientForm, DonorTestForm, RecipientTestForm
from .mixins import SuperAdminRequiredMixin, superadmin_required
from .details import parse_number_list_from_string, donor_detail, recipient_detail
from .pcr import extract_patient_info_from_pdf, extract_alleles_from_pdf
from .analysis import analysis_recipients

CustomUser = get_user_model()

class SignUpView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user_list')

@login_required
def main(request):
    cadaver_donors = CadaverDonor.objects.all()
    living_donors = LivingDonor.objects.all()
    donors = list(chain(cadaver_donors, living_donors))[:5]
    recipients = Recipient.objects.all()[:5]


    context = {
        'donors': donors,
        'recipients': recipients
    }

    return render(request, 'main.html', context=context)

class DonorListView(LoginRequiredMixin, ListView):
    template_name = 'donors/donor_list.html'
    paginate_by = 100
    context_object_name = 'donors'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        blood_group = self.request.GET.get('blood_group')
        national_code = self.request.GET.get('national_code')
        age = self.request.GET.get('age')

        filters = {}
        if blood_group:
            filters['blood_group'] = blood_group
        if national_code:
            filters['national_code'] = national_code
        if age:
            filters['age'] = age

        cadaver_donors = CadaverDonor.objects.filter(**filters)
        living_donors = LivingDonor.objects.filter(**filters)

        if search_query:
            cadaver_donors = cadaver_donors.filter(Q(full_name__icontains=search_query))
            living_donors = living_donors.filter(Q(full_name__icontains=search_query))

        combined = list(chain(cadaver_donors, living_donors))
        return combined

class CadaverDonorCreateView(LoginRequiredMixin, CreateView):
    model = CadaverDonor
    form_class = CadaverDonorForm
    template_name = 'donors/cadaver_donor_add.html'

    def get_success_url(self):
        return reverse('cadaver_donor_detail', kwargs={'pk': self.object.id})

@login_required
def all_cadaver_donor_detail(request, pk):
    cadaver_donor = get_object_or_404(CadaverDonor, pk=pk)
    recipient_list = Recipient.objects.all()
    context = donor_detail(request, cadaver_donor, recipient_list, status=0)

    return render(request, 'donors/donor_detail.html', context)

@login_required
def some_cadaver_donor_detail(request, pk):
    some_recipients = request.GET.get('some_recipients')
    cadaver_donor = get_object_or_404(CadaverDonor, pk=pk)
    recipient_list = Recipient.objects.filter(id__in=parse_number_list_from_string(some_recipients))
    context = donor_detail(request, cadaver_donor, recipient_list, status=1)

    return render(request, 'donors/donor_detail.html', context)

class CadaverDonorUpdateView(LoginRequiredMixin, UpdateView):
    model = CadaverDonor
    form_class = CadaverDonorForm
    template_name = 'donors/cadaver_donor_form.html'

    def get_success_url(self):
        return reverse('cadaver_donor_detail', kwargs={'pk': self.object.id})

class CadaverDonorDeleteView(LoginRequiredMixin, DeleteView):
    model = CadaverDonor
    context_object_name = 'donor'
    template_name = 'donors/cadaver_donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')

class LivingDonorCreateView(LoginRequiredMixin, CreateView):
    model = LivingDonor
    form_class = LivingDonorForm
    template_name = 'donors/living_donor_add.html'

    def get_success_url(self):
        return reverse('living_donor_detail', kwargs={'pk': self.object.id})

@login_required
def all_living_donor_detail(request, pk):
    living_donor = get_object_or_404(LivingDonor, pk=pk)
    recipient_list = Recipient.objects.all()
    context = donor_detail(request, living_donor, recipient_list, status=0)

    return render(request, 'donors/donor_detail.html', context)

@login_required
def some_living_donor_detail(request, pk):
    some_recipients = request.GET.get('some_recipients')
    living_donor = get_object_or_404(LivingDonor, pk=pk)
    recipient_list = Recipient.objects.filter(id__in=parse_number_list_from_string(some_recipients))
    context = donor_detail(request, living_donor, recipient_list, status=1)

    return render(request, 'donors/donor_detail.html', context)

class LivingDonorUpdateView(LoginRequiredMixin, UpdateView):
    model = LivingDonor
    form_class = LivingDonorForm
    template_name = 'donors/living_donor_form.html'

    def get_success_url(self):
        return reverse('living_donor_detail', kwargs={'pk': self.object.id})

class LivingDonorDeleteView(LoginRequiredMixin, DeleteView):
    model = LivingDonor
    context_object_name = 'donor'
    template_name = 'donors/living_donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'
    context_object_name = 'recipients'
    ordering = 'id'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        blood_group = self.request.GET.get('blood_group')
        national_code = self.request.GET.get('national_code')
        age = self.request.GET.get('age')

        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query)
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
    template_name = 'recipients/recipient_add.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        if form.cleaned_data.get('read_uam_from') == '2':
            self.object.process_uam_data()

        return response

    def get_success_url(self):
        return reverse('recipient_detail', kwargs={'pk': self.object.id})

@login_required
def all_recipient_detail(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    cadaver_donor_list = CadaverDonor.objects.all()
    living_donor_list = LivingDonor.objects.all()
    context = recipient_detail(request, recipient, cadaver_donor_list, living_donor_list,  status=0)

    return render(request, 'recipients/recipient_detail.html', context)

@login_required
def some_recipient_detail(request, pk):
    some_cadaver_donors = request.GET.get('some_cadaver_donors')
    some_living_donors = request.GET.get('some_living_donors')
    recipient = get_object_or_404(Recipient, pk=pk)
    cadaver_donor_list = CadaverDonor.objects.filter(id__in=parse_number_list_from_string(some_cadaver_donors))
    living_donor_list = LivingDonor.objects.filter(id__in=parse_number_list_from_string(some_living_donors))
    context = recipient_detail(request, recipient, cadaver_donor_list, living_donor_list,  status=1)

    return render(request, 'recipients/recipient_detail.html', context)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/recipient_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        if form.cleaned_data.get('read_uam_from') == '2':
            self.object.process_uam_data()

        return response

    def get_success_url(self):
        return reverse('recipient_detail', kwargs={'pk': self.object.id})

class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipients/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')

def select_donors_for_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)

    return render(request, 'donors/select_donors.html', {'recipient': recipient})

def select_recipients_for_cadaver_donor(request, pk):
    donor = get_object_or_404(CadaverDonor, pk=pk)

    return render(request, 'recipients/select_recipients.html', {'donor': donor})

def select_recipients_for_living_donor(request, pk):
    donor = get_object_or_404(LivingDonor, pk=pk)

    return render(request, 'recipients/select_recipients.html', {'donor': donor})

@login_required
def cadaver_donor_api(request):
    query = request.GET.get('full_name', '')
    cadaver_donors = CadaverDonor.objects.filter(full_name__icontains=query)
    cadaver_donors_list = []

    for donor in cadaver_donors:
        cadaver_donors_list.append({
            'id': donor.id,
            'full_name': donor.full_name,
            'national_code': donor.national_code,
            'phone_number': donor.phone_number
        })
        
    return JsonResponse(cadaver_donors_list, safe=False)

@login_required
def living_donor_api(request):
    query = request.GET.get('full_name', '')
    living_donors = LivingDonor.objects.filter(full_name__icontains=query)
    living_donors_list = []

    for donor in living_donors:
        living_donors_list.append({
            'id': donor.id,
            'full_name': donor.full_name,
            'national_code': donor.national_code,
            'phone_number': donor.phone_number
        })
        
    return JsonResponse(living_donors_list, safe=False)

@login_required
def recipient_api(request):
    query = request.GET.get('full_name', '')
    recipients = Recipient.objects.filter(full_name__icontains=query)
    recipients_list = []

    for recipient in recipients:
        recipients_list.append({
            'id': recipient.id,
            'full_name': recipient.full_name,
            'national_code': recipient.national_code,
            'phone_number': recipient.phone_number
        })
        
    return JsonResponse(recipients_list, safe=False)

@login_required
@superadmin_required
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

class HlaACreateview(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = HlaA
    fields = '__all__'
    template_name = 'hla/hla_a_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaAUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = HlaA
    fields = '__all__'
    template_name = 'hla/hla_a_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaADeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = HlaA
    template_name = 'hla/hla_a_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaBCreateview(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = HlaB
    fields = '__all__'
    template_name = 'hla/hla_b_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaBUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = HlaB
    fields = '__all__'
    template_name = 'hla/hla_b_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaBDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = HlaB
    template_name = 'hla/hla_b_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDRB1Createview(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = HlaDRB1
    fields = '__all__'
    template_name = 'hla/hla_drb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRB1UpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = HlaDRB1
    fields = '__all__'
    template_name = 'hla/hla_drb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRB1DeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = HlaDRB1
    template_name = 'hla/hla_drb1_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDRBCreateview(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = HlaDRB
    fields = '__all__'
    template_name = 'hla/hla_drb_form.html'

    def get_success_url(self):
        return reverse('hla_lists')
    
class HlaDRBUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = HlaDRB
    fields = '__all__'
    template_name = 'hla/hla_drb_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDRBDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = HlaDRB
    template_name = 'hla/hla_drb_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

class HlaDQB1Createview(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = HlaDQB1
    fields = '__all__'
    template_name = 'hla/hla_dqb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDQB1UpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = HlaDQB1
    fields = '__all__'
    template_name = 'hla/hla_dqb1_form.html'

    def get_success_url(self):
        return reverse('hla_lists')

class HlaDQB1DeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = HlaDQB1
    template_name = 'hla/hla_dqb1_confirm_delete.html'
    success_url = reverse_lazy('hla_lists')

@login_required
@superadmin_required
def referees_test_lists(request):
    donor_tests = DonorTest.objects.all()
    recipient_tests = RecipientTest.objects.all()

    donor_test_selected = None
    recipient_test_selected = None

    rdts = request.GET.get('donor_test_selected')
    rrts = request.GET.get('recipient_test_selected')

    if rdts and rrts:
        donor_test_selected = donor_tests.get(id=rdts)
        recipient_test_selected = recipient_tests.get(id=rrts)

    context = {
        'donor_tests': donor_tests,
        'recipient_tests': recipient_tests,
        'donor': donor_test_selected,
        'recipient': recipient_test_selected,
    }

    return render(request, 'test/referees_test_lists.html', context)

class DonorTestCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = DonorTest
    form_class = DonorTestForm
    template_name = 'test/donor_test_add.html'

    def get_success_url(self):
        return reverse('referees_test_lists')

class RecipientTestCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = RecipientTest
    form_class = RecipientTestForm
    template_name = 'test/recipient_test_add.html'

    def get_success_url(self):
        return reverse('referees_test_lists')

class DonorTestUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = DonorTest
    form_class = DonorTestForm
    template_name = 'test/donor_test_add.html'

    def get_success_url(self):
        return reverse('referees_test_lists')

class RecipientTestUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = RecipientTest
    form_class = RecipientTestForm
    template_name = 'test/recipient_test_add.html'

    def get_success_url(self):
        return reverse('referees_test_lists')
    
class DonorTestDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = DonorTest
    template_name = 'test/donor_test_confirm_delete.html'
    success_url = reverse_lazy('referees_test_lists')

class RecipientTestDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = RecipientTest
    template_name = 'test/recipient_test_confirm_delete.html'
    success_url = reverse_lazy('referees_test_lists')

class UserListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    paginate_by = 100
    template_name = 'users/user_list.html'

class UserUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse('user_list')

class UserDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@csrf_exempt
@login_required
def extract_info_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        data = extract_patient_info_from_pdf(pdf_file)
        return JsonResponse(data)
    return JsonResponse({'error': 'فایل ارسال نشده'}, status=400)

@csrf_exempt
@login_required
def extract_hla_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        data = extract_alleles_from_pdf(pdf_file)
        return JsonResponse(data)
    return JsonResponse({'error': 'فایل ارسال نشده'}, status=400)

@login_required
@superadmin_required
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
        ('B*73', '3'), ('B*78', '3'), ('B*81', '3'), ('B*82', '3'),
    ]

    hla_drb_choices = [
        'DRB3',
        'DRB4',
        'DRB5',
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
    
    for value in hla_drb_choices:
        HlaDRB.objects.create(value=value)

    for value, type_ in hla_drb1_choices:
        HlaDRB1.objects.create(value=value, type=type_)

    for value, type_ in hla_dqb1_choices:
        HlaDQB1.objects.create(value=value, type=type_)

    return redirect('main')
