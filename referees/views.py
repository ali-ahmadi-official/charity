from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import (
    CadaverDonor, LivingDonor, Recipient, HlaA, HlaB, HlaDRB1,
    HlaDRB, HlaDQB1, DonorTest, RecipientTest, HistoryCall, RecipientUAMMFI
)
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, CadaverDonorForm, LivingDonorForm,
    RecipientForm, DonorTestForm, RecipientTestForm, HistoryCallForm, HistoryCallUpdateForm,
    AddGroupToDonorsForm, AddGroupToRecipientsForm
)
from .mixins import SuperAdminRequiredMixin, superadmin_required
from .details import parse_number_list_from_string, donor_detail, recipient_detail, get_donors_without_uams
from .pcr import extract_patient_info_from_pdf, extract_alleles_from_pdf
from .analysis import analysis_recipients, analysis_donors, merge_analysis_results
from .excel_exporter import export_to_excel

CustomUser = get_user_model()

HLA_FIELDS = ['hla_a', 'hla_b', 'hla_drb1', 'hla_drb', 'hla_dqb1']

def owner_filter(user, queryset):
    base_filter = Q(is_test=user.is_staff)

    if not user.groups.all():
        return queryset.filter(base_filter)

    return queryset.filter(
        base_filter & Q(creator_groups__in=user.groups.all())
    ).distinct()

class SignUpView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user_list')

@login_required
def main(request):
    cadaver_donors = owner_filter(request.user, CadaverDonor.objects.all())
    living_donors = owner_filter(request.user, LivingDonor.objects.all())
    donors = list(chain(cadaver_donors, living_donors))[:5]
    recipients = owner_filter(request.user, Recipient.objects.all())[:5]

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

        cadaver_donors = owner_filter(self.request.user, CadaverDonor.objects.filter(**filters))
        living_donors = owner_filter(self.request.user, LivingDonor.objects.filter(**filters))

        if search_query:
            cadaver_donors = cadaver_donors.filter(Q(full_name__icontains=search_query))
            living_donors = living_donors.filter(Q(full_name__icontains=search_query))

        combined = list(chain(cadaver_donors, living_donors))
        return combined

class CadaverDonorCreateView(LoginRequiredMixin, CreateView):
    model = CadaverDonor
    form_class = CadaverDonorForm
    template_name = 'donors/cadaver_donor_add.html'

    def form_valid(self, form):
        instance = form.save(commit=False)

        if self.request.user.is_staff:
            instance.is_test = True

        instance.creator_user = self.request.user
        instance.save()

        form.save_m2m()
        instance.creator_groups.set(self.request.user.groups.all())

        self.object = instance
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('cadaver_donor_detail', kwargs={'pk': self.object.id})

@login_required
def all_cadaver_donor_detail(request, pk):
    cadaver_donor = get_object_or_404(CadaverDonor, pk=pk)
    recipient_list = owner_filter(request.user, Recipient.objects.exclude(search_donor='3').filter(deactivate=False))
    context = donor_detail(request, cadaver_donor, recipient_list, status=0)

    return render(request, 'donors/donor_detail.html', context)

@login_required
def some_cadaver_donor_detail(request, pk):
    some_recipients = request.GET.get('some_recipients')
    cadaver_donor = get_object_or_404(CadaverDonor, pk=pk)
    recipient_list = owner_filter(request.user, Recipient.objects.filter(id__in=parse_number_list_from_string(some_recipients)).exclude(search_donor='3'))
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

    def form_valid(self, form):
        instance = form.save(commit=False)
    
        if self.request.user.is_staff:
            instance.is_test = True
    
        instance.creator_user = self.request.user
        instance.save()
    
        form.save_m2m()
        instance.creator_groups.set(self.request.user.groups.all())
    
        self.object = instance
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('living_donor_detail', kwargs={'pk': self.object.id})

@login_required
def all_living_donor_detail(request, pk):
    living_donor = get_object_or_404(LivingDonor, pk=pk)
    recipient_list = owner_filter(request.user, Recipient.objects.exclude(search_donor='2').filter(deactivate=False))
    context = donor_detail(request, living_donor, recipient_list, status=0)

    return render(request, 'donors/donor_detail.html', context)

@login_required
def some_living_donor_detail(request, pk):
    some_recipients = request.GET.get('some_recipients')
    living_donor = get_object_or_404(LivingDonor, pk=pk)
    recipient_list = owner_filter(request.user, Recipient.objects.filter(id__in=parse_number_list_from_string(some_recipients)).exclude(search_donor='2'))
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
        queryset = owner_filter(self.request.user, queryset)
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

        if self.request.user.is_staff:
            self.object.is_test = True

        self.object.creator_user = self.request.user
        self.object.save()

        self.object.creator_groups.set(self.request.user.groups.all())

        if form.cleaned_data.get("read_uam_from") == "2":
            self.object.process_uam_data()
            self.object.save()

        return response

    def get_success_url(self):
        return reverse('recipient_detail', kwargs={'pk': self.object.id})

@login_required
def all_recipient_detail(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    cadaver_donor_list = owner_filter(request.user, CadaverDonor.objects.filter(deactivate=False))
    living_donor_list = owner_filter(request.user, LivingDonor.objects.filter(deactivate=False))
    context = recipient_detail(request, recipient, cadaver_donor_list, living_donor_list,  status=0)

    return render(request, 'recipients/recipient_detail.html', context)

@login_required
def some_recipient_detail(request, pk):
    some_cadaver_donors = request.GET.get('some_cadaver_donors')
    some_living_donors = request.GET.get('some_living_donors')
    recipient = get_object_or_404(Recipient, pk=pk)
    cadaver_donor_list = owner_filter(request.user, CadaverDonor.objects.filter(id__in=parse_number_list_from_string(some_cadaver_donors)))
    living_donor_list = owner_filter(request.user, LivingDonor.objects.filter(id__in=parse_number_list_from_string(some_living_donors)))
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

class RecipientUAMMFIView(LoginRequiredMixin, View):
    template_name = 'recipients/recipient_uam_mfi.html'

    def get_uam_items(self, recipient):
        existing = {}
        for m in recipient.uam_mfi_values.all():
            for field in ['hla_a', 'hla_b', 'hla_drb1', 'hla_drb', 'hla_dqb1']:
                hla_id = getattr(m, f'{field}_id')
                if hla_id:
                    existing[(field, hla_id)] = m

        field_map = [
            ('hla_a', recipient.hla_a_uam.all()),
            ('hla_b', recipient.hla_b_uam.all()),
            ('hla_drb1', recipient.hla_drb1_uam.all()),
            ('hla_drb', recipient.hla_drb_uam.all()),
            ('hla_dqb1', recipient.hla_dqb1_uam.all()),
        ]

        items = []
        for field, qs in field_map:
            for hla in qs:
                mfi_obj = existing.get((field, hla.id))
                items.append({
                    'field': field,
                    'hla_id': hla.id,
                    'value': hla.value,
                    'mfi': mfi_obj.mfi if mfi_obj else '',
                    'input_name': f'mfi__{field}__{hla.id}',
                })
        return items

    def get(self, request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        items = self.get_uam_items(recipient)
        return render(request, self.template_name, {'recipient': recipient, 'items': items})

    def post(self, request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        items = self.get_uam_items(recipient)
        valid_keys = {(i['field'], i['hla_id']) for i in items}

        for key, value in request.POST.items():
            if not key.startswith('mfi__'):
                continue
            try:
                _, field, hla_id = key.split('__')
                hla_id = int(hla_id)
            except ValueError:
                continue

            if (field, hla_id) not in valid_keys:
                continue

            value = value.strip()
            lookup = {'recipient': recipient, f'{field}_id': hla_id}

            if value == '':
                RecipientUAMMFI.objects.filter(**lookup).delete()
                continue

            try:
                mfi_val = int(value)
            except ValueError:
                continue

            RecipientUAMMFI.objects.update_or_create(**lookup, defaults={'mfi': mfi_val})

        return redirect('recipient_detail', pk=recipient.pk)

class RecipientUAMFilterImpactView(View):
    template_name = 'recipients/recipient_uam_filter_impact.html'

    def get(self, request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        cadaver_donor_list = owner_filter(request.user, CadaverDonor.objects.filter(deactivate=False))
        living_donor_list = owner_filter(request.user, LivingDonor.objects.filter(deactivate=False))

        uam_items = []
        for m in recipient.uam_mfi_values.select_related(*HLA_FIELDS).order_by('mfi'):
            field = next(f for f in HLA_FIELDS if getattr(m, f'{f}_id'))
            hla_id = getattr(m, f'{field}_id')
            uam_items.append({
                'value': m.hla.value,
                'mfi': m.mfi,
                'checkbox_value': f'{field}:{hla_id}',
            })

        selected = request.GET.getlist('uam')
        addable_donors = None

        if selected:
            selections = []
            valid_values = {item['checkbox_value'] for item in uam_items}
            for s in selected:
                if s in valid_values:
                    field, hla_id = s.split(':')
                    selections.append((field, int(hla_id)))

            if selections:
                base_context = recipient_detail(request, recipient, cadaver_donor_list, living_donor_list, status=0)
                base_keys = {(type(d).__name__, d.id) for d in base_context['donors']}

                without_donors = get_donors_without_uams(request, recipient, cadaver_donor_list, living_donor_list, selections)
                addable_donors = [d for d in without_donors if (type(d).__name__, d.id) not in base_keys]

        context = {
            'recipient': recipient,
            'uam_items': uam_items,
            'selected_values': selected,
            'addable_donors': addable_donors,
            'form_submitted': bool(selected),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        selected = request.POST.getlist('uam')

        valid_map = {}
        for m in recipient.uam_mfi_values.all():
            for f in HLA_FIELDS:
                hla_id = getattr(m, f'{f}_id')
                if hla_id:
                    valid_map[f'{f}:{hla_id}'] = m

        updated = 0
        for s in selected:
            m = valid_map.get(s)
            if m and m.participates_in_filter:
                m.participates_in_filter = False
                m.save(update_fields=['participates_in_filter'])
                updated += 1

        return redirect('recipient_detail', pk=recipient.pk)

@login_required
def select_donors_for_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk, is_test=request.user.is_staff)

    return render(request, 'donors/select_donors.html', {'recipient': recipient})

@login_required
def select_recipients_for_cadaver_donor(request, pk):
    donor = get_object_or_404(CadaverDonor, pk=pk, is_test=request.user.is_staff)

    return render(request, 'recipients/select_recipients.html', {'donor': donor})

@login_required
def select_recipients_for_living_donor(request, pk):
    donor = get_object_or_404(LivingDonor, pk=pk, is_test=request.user.is_staff)

    return render(request, 'recipients/select_recipients.html', {'donor': donor})

@login_required
def cadaver_donor_api(request):
    query = request.GET.get('full_name', '')
    cadaver_donors = owner_filter(request.user, CadaverDonor.objects.filter(full_name__icontains=query))
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
    living_donors = owner_filter(request.user, LivingDonor.objects.filter(full_name__icontains=query))
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
    recipients = owner_filter(request.user, Recipient.objects.filter(full_name__icontains=query))
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
    donor_tests = owner_filter(request.user, DonorTest.objects.all())
    recipient_tests = owner_filter(request.user, RecipientTest.objects.all())

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

    def form_valid(self, form):
        instance = form.save(commit=False)

        if self.request.user.is_staff:
            instance.is_test = True

        instance.creator_user = self.request.user
        instance.save()

        form.save_m2m()
        instance.creator_groups.set(self.request.user.groups.all())

        self.object = instance
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('referees_test_lists')

class RecipientTestCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = RecipientTest
    form_class = RecipientTestForm
    template_name = 'test/recipient_test_add.html'

    def form_valid(self, form):
        instance = form.save(commit=False)

        if self.request.user.is_staff:
            instance.is_test = True

        instance.creator_user = self.request.user
        instance.save()

        form.save_m2m()
        instance.creator_groups.set(self.request.user.groups.all())

        self.object = instance
        return HttpResponseRedirect(self.get_success_url())

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

class HistoryCallListView(LoginRequiredMixin, ListView):
    model = HistoryCall
    template_name = 'history_call/list.html'
    context_object_name = 'history_calls'

    def get_queryset(self):
        recipient_id = self.kwargs.get("recipient_id")
        return HistoryCall.objects.filter(recipient__id=recipient_id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient_id = self.kwargs.get("recipient_id")
        context['recipient'] = get_object_or_404(Recipient, id=recipient_id)
        return context

class HistoryCallCreateView(LoginRequiredMixin, CreateView):
    model = HistoryCall
    form_class = HistoryCallForm
    template_name = 'history_call/form.html'
    
    def form_valid(self, form):
        recipient_id = self.kwargs.get("recipient_id")
        recipient = get_object_or_404(Recipient, id=recipient_id)

        form.instance.recipient = recipient
        response = super().form_valid(form)

        self.object.process_uam_data()
        return response

    def get_success_url(self):
        recipient_id = self.kwargs.get("recipient_id")
        return reverse("history_call_list", args=[recipient_id])
    
class HistoryCallUpdateView(LoginRequiredMixin, UpdateView):
    model = HistoryCall
    form_class = HistoryCallUpdateForm
    template_name = 'history_call/form.html'

    def get_success_url(self):
        return reverse("history_call_list", args=[self.kwargs.get("recipient_id")])

class HistoryCallDeleteView(LoginRequiredMixin, DeleteView):
    model = HistoryCall
    template_name = 'history_call/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient_id = self.kwargs.get("recipient_id")
        context['recipient'] = get_object_or_404(Recipient, id=recipient_id)
        return context

    def get_success_url(self):
        return reverse("history_call_list", args=[self.kwargs.get("recipient_id")])

class UserListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = CustomUser
    context_object_name = "users"
    paginate_by = 100
    template_name = "users/user_list.html"

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.all()

        if user.id == 1:
            return CustomUser.objects.all()

        return CustomUser.objects.filter(
            groups__in=user_groups
        ).distinct()

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

class GroupListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = Group
    context_object_name = "groups"
    paginate_by = 100
    template_name = "groups/group_list.html"

    def get_queryset(self):
        groups = Group.objects.prefetch_related(
            "livingdonor_set",
            "cadaverdonor_set",
            "recipient_set",
        )

        for group in groups:
            donor_only = donor_shared = 0
            donors = (
                list(group.livingdonor_set.all()) +
                list(group.cadaverdonor_set.all())
            )

            for donor in donors:
                if donor.creator_groups.count() == 1:
                    donor_only += 1
                else:
                    donor_shared += 1

            recipient_only = recipient_shared = 0

            for recipient in group.recipient_set.all():
                if recipient.creator_groups.count() == 1:
                    recipient_only += 1
                else:
                    recipient_shared += 1

            group.donor_only = donor_only
            group.donor_shared = donor_shared
            group.recipient_only = recipient_only
            group.recipient_shared = recipient_shared

        return groups

class GroupCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = Group
    fields = ["name"]
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")

class GroupUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = Group
    fields = ["name"]
    template_name = "groups/group_form.html"

    def get_success_url(self):
        return reverse("group_list")

class GroupDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_confirm_delete.html"
    success_url = reverse_lazy("group_list")

class AddGroupToDonorsView(LoginRequiredMixin, SuperAdminRequiredMixin, FormView):
    template_name = "donors/add_group.html"
    form_class = AddGroupToDonorsForm
    success_url = reverse_lazy("donor_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        living_donors = form.cleaned_data["living_donors"]
        cadaver_donors = form.cleaned_data["cadaver_donors"]
        group = form.cleaned_data["group"]

        for donor in living_donors:
            donor.creator_groups.add(group)

        for donor in cadaver_donors:
            donor.creator_groups.add(group)

        return super().form_valid(form)

class AddGroupToRecipientsView(LoginRequiredMixin, SuperAdminRequiredMixin, FormView):
    template_name = "recipients/add_group.html"
    form_class = AddGroupToRecipientsForm
    success_url = reverse_lazy("recipient_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        recipients = form.cleaned_data["recipients"]
        group = form.cleaned_data["group"]

        for recipient in recipients:
            recipient.creator_groups.add(group)

        return super().form_valid(form)

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

@login_required
def r_analysis(request):
    recipients = owner_filter(request.user, Recipient.objects.all())
    deactivate = "all"
    if request.GET.get("deactivate") == "yes":
        recipients = recipients.filter(deactivate=True)
        deactivate = "yes"
    elif request.GET.get("deactivate") == "no":
        recipients = recipients.filter(deactivate=False)
        deactivate = "no"

    results = analysis_recipients(recipients)

    if request.GET.get("export") == "excel":
        return export_to_excel(
            datasets=[
                results['gender_status'],
                results['age_status'],
                results['blood_group_status'],
                results['previous_donation'],
                results['medical_urgency'],
                results['candidate_for_2_kidney_TX'],
                results['candidate_for_kidney_after_other_organ_TX'],
                results['cpra'],
                results['desensitized'],
                results['hla_a'],
                results['hla_b'],
                results['hla_drb1'],
                results['hla_drb'],
                results['hla_dqb1'],
                results['hla_a_uam'],
                results['hla_b_uam'],
                results['hla_drb1_uam'],
                results['hla_drb_uam'],
                results['hla_dqb1_uam'],
            ],
            sheet_names=[
                'جنسیت',
                'بازه سنی',
                'گروه خونی',
                'Previous Donation',
                'Medical Urgency',
                'Candidate For 2 Kidney TX',
                'Candidate For Kidney After...',
                'CPRA',
                'Desensitized',
                'HLA A',
                'HLA B',
                'HLA DRB1',
                'HLA DRB',
                'HLA DQB1',
                'HLA A UAM',
                'HLA B UAM',
                'HLA DRB1 UAM',
                'HLA DRB UAM',
                'HLA DQB1 UAM',
            ],
            filename=f"recipients_analysis.xlsx",
        )

    return render(request, 'analysis/r_analysis.html', {'results': results, 'deactivate': deactivate})

@login_required
def d_analysis(request):
    cadaver_donors = owner_filter(request.user, CadaverDonor.objects.all())
    living_donors = owner_filter(request.user, LivingDonor.objects.all())
    deactivate = "all"
    if request.GET.get("deactivate") == "yes":
        cadaver_donors = cadaver_donors.filter(deactivate=True)
        living_donors = living_donors.filter(deactivate=True)
        deactivate = "yes"
    elif request.GET.get("deactivate") == "no":
        cadaver_donors = cadaver_donors.filter(deactivate=False)
        living_donors = living_donors.filter(deactivate=False)
        deactivate = "no"

    cadaver_donors_results = analysis_donors(cadaver_donors)
    living_donors_results = analysis_donors(living_donors)
    results = merge_analysis_results(cadaver_donors_results, living_donors_results)

    if request.GET.get("export") == "excel":
        return export_to_excel(
            datasets=[
                results['gender_status'],
                results['age_status'],
                results['blood_group_status'],
                results['hla_a'],
                results['hla_b'],
                results['hla_drb1'],
                results['hla_drb'],
                results['hla_dqb1'],
            ],
            sheet_names=[
                'جنسیت',
                'بازه سنی',
                'گروه خونی',
                'HLA A',
                'HLA B',
                'HLA DRB1',
                'HLA DRB',
                'HLA DQB1',
            ],
            filename=f"donors_analysis.xlsx",
        )

    return render(request, 'analysis/d_analysis.html', {'results': results, 'deactivate': deactivate})
