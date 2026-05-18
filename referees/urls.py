from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from .views import (
    SignUpView,
    main,
    DonorListView, 
    CadaverDonorCreateView, all_cadaver_donor_detail, some_cadaver_donor_detail, CadaverDonorUpdateView, CadaverDonorDeleteView,
    LivingDonorCreateView, all_living_donor_detail, some_living_donor_detail, LivingDonorUpdateView, LivingDonorDeleteView,
    RecipientListView, RecipientCreateView, all_recipient_detail, some_recipient_detail, RecipientUpdateView, RecipientDeleteView,
    select_donors_for_recipient, select_recipients_for_cadaver_donor, select_recipients_for_living_donor,
    cadaver_donor_api ,living_donor_api, recipient_api,
    hla_lists, 
    HlaACreateview, HlaAUpdateView, HlaADeleteView,
    HlaBCreateview, HlaBUpdateView, HlaBDeleteView,
    HlaDRB1Createview, HlaDRB1UpdateView, HlaDRB1DeleteView,
    HlaDRBCreateview, HlaDRBUpdateView, HlaDRBDeleteView,
    HlaDQB1Createview, HlaDQB1UpdateView, HlaDQB1DeleteView,
    referees_test_lists, DonorTestCreateView, RecipientTestCreateView, DonorTestUpdateView, RecipientTestUpdateView, DonorTestDeleteView, RecipientTestDeleteView,
    HistoryCallListView, HistoryCallCreateView, HistoryCallUpdateView, HistoryCallDeleteView,
    UserListView, UserUpdateView, UserDeleteView,
    extract_info_data, extract_hla_data,
    auto_add_hla,
    r_analysis, d_analysis
)

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', main, name='main'),

    path('donors/', DonorListView.as_view(), name='donor_list'),

    path('cadaver-donors/new/', CadaverDonorCreateView.as_view(), name='cadaver_donor_create'),
    path('cadaver-donors/<int:pk>/', all_cadaver_donor_detail, name='cadaver_donor_detail'),
    path('cadaver-donors/<int:pk>/special-analysis/', some_cadaver_donor_detail, name='some_cadaver_donor_detail'),
    path('cadaver-donors/<int:pk>/edit/', CadaverDonorUpdateView.as_view(), name='cadaver_donor_update'),
    path('cadaver-donors/<int:pk>/delete/', CadaverDonorDeleteView.as_view(), name='cadaver_donor_delete'),

    path('living-donors/new/', LivingDonorCreateView.as_view(), name='living_donor_create'),
    path('living-donors/<int:pk>/', all_living_donor_detail, name='living_donor_detail'),
    path('living-donors/<int:pk>/special-analysis/', some_living_donor_detail, name='some_living_donor_detail'),
    path('living-donors/<int:pk>/edit/', LivingDonorUpdateView.as_view(), name='living_donor_update'),
    path('living-donors/<int:pk>/delete/', LivingDonorDeleteView.as_view(), name='living_donor_delete'),

    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/', all_recipient_detail, name='recipient_detail'),
    path('recipients/<int:pk>/special-analysis/', some_recipient_detail, name='some_recipient_detail'),
    path('recipients/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('cadaver-donors/select-recipients-for-cadaver-donor/<int:pk>/', select_recipients_for_cadaver_donor, name='select_recipients_for_cadaver_donor'),
    path('living-donors/select-recipients-for-living-donor/<int:pk>/', select_recipients_for_living_donor, name='select_recipients_for_living_donor'),
    path('recipients/select-donors-for-recipient/<int:pk>/', select_donors_for_recipient, name='select_donors_for_recipient'),

    path('cadaver-donor-api/', cadaver_donor_api, name='cadaver_donor_api'),
    path('living-donor-api/', living_donor_api, name='living_donor_api'),
    path('recipient-api/', recipient_api, name='recipient_api'),

    path('hla-list/', hla_lists, name='hla_lists'),

    path('hla-list/hla-a/new/', HlaACreateview.as_view(), name='hla_a_create'),
    path('hla-list/hla-a/<int:pk>/edit/', HlaAUpdateView.as_view(), name='hla_a_update'),
    path('hla-list/hla-a/<int:pk>/delete/', HlaADeleteView.as_view(), name='hla_a_delete'),

    path('hla-list/hla-b/new/', HlaBCreateview.as_view(), name='hla_b_create'),
    path('hla-list/hla-b/<int:pk>/edit/', HlaBUpdateView.as_view(), name='hla_b_update'),
    path('hla-list/hla-b/<int:pk>/delete/', HlaBDeleteView.as_view(), name='hla_b_delete'),

    path('hla-list/hla-drb1/new/', HlaDRB1Createview.as_view(), name='hla_drb1_create'),
    path('hla-list/hla-drb1/<int:pk>/edit/', HlaDRB1UpdateView.as_view(), name='hla_drb1_update'),
    path('hla-list/hla-drb1/<int:pk>/delete/', HlaDRB1DeleteView.as_view(), name='hla_drb1_delete'),

    path('hla-list/hla-drb/new/', HlaDRBCreateview.as_view(), name='hla_drb_create'),
    path('hla-list/hla-drb/<int:pk>/edit/', HlaDRBUpdateView.as_view(), name='hla_drb_update'),
    path('hla-list/hla-drb/<int:pk>/delete/', HlaDRBDeleteView.as_view(), name='hla_drb_delete'),

    path('hla-list/hla-dqb1/new/', HlaDQB1Createview.as_view(), name='hla_dqb1_create'),
    path('hla-list/hla-dqb1/<int:pk>/edit/', HlaDQB1UpdateView.as_view(), name='hla_dqb1_update'),
    path('hla-list/hla-dqb1/<int:pk>/delete/', HlaDQB1DeleteView.as_view(), name='hla_dqb1_delete'),

    path('hla-test/', referees_test_lists, name='referees_test_lists'),
    path('hla-test/donor/new/', DonorTestCreateView.as_view(), name='donor_test_create'),
    path('hla-test/donor/<int:pk>/edit/', DonorTestUpdateView.as_view(), name='donor_test_update'),
    path('hla-test/donor/<int:pk>/delete/', DonorTestDeleteView.as_view(), name='donor_test_delete'),
    path('hla-test/recipient/new/', RecipientTestCreateView.as_view(), name='recipient_test_create'),
    path('hla-test/recipient/<int:pk>/edit/', RecipientTestUpdateView.as_view(), name='recipient_test_update'),
    path('hla-test/recipient/<int:pk>/delete/', RecipientTestDeleteView.as_view(), name='recipient_test_delete'),

    path('recipients/history-call/<int:recipient_id>/list/', HistoryCallListView.as_view(), name='history_call_list'),
    path('recipients/history-call/<int:recipient_id>/new/', HistoryCallCreateView.as_view(), name='history_call_create'),
    path('recipients/history-call/<int:recipient_id>/edit/<int:pk>/', HistoryCallUpdateView.as_view(), name='history_call_update'),
    path('recipients/history-call/<int:recipient_id>/delete/<int:pk>/', HistoryCallDeleteView.as_view(), name='history_call_delete'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    path('api/extract-info/', extract_info_data, name='extract_info_data'),
    path('api/extract-hla/', extract_hla_data, name='extract_hla_data'),

    path('auto-add-hla/', auto_add_hla, name='auto_add_hla'),
    path('recipients/analysis/', r_analysis, name='r_analysis'),
    path('donors/analysis/', d_analysis, name='d_analysis'),
]