from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    main,
    DonorListView, DonorCreateView, donor_detail, DonorUpdateView, DonorDeleteView,
    RecipientListView, RecipientCreateView, recipient_detail, RecipientUpdateView, RecipientDeleteView,
    hla_lists, 
    HlaACreateview, HlaAUpdateView, HlaADeleteView,
    HlaBCreateview, HlaBUpdateView, HlaBDeleteView,
    HlaDRB1Createview, HlaDRB1UpdateView, HlaDRB1DeleteView,
    HlaDRBCreateview, HlaDRBUpdateView, HlaDRBDeleteView,
    HlaDQB1Createview, HlaDQB1UpdateView, HlaDQB1DeleteView,
    referees_test_lists, DonorTestCreateView, RecipientTestCreateView, DonorTestUpdateView, RecipientTestUpdateView, DonorTestDeleteView, RecipientTestDeleteView,
    auto_add_hla,
)

urlpatterns = [
    path('', main, name='main'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('donors/', DonorListView.as_view(), name='donor_list'),
    path('donors/new/', DonorCreateView.as_view(), name='donor_create'),
    path('donors/<int:pk>/', donor_detail, name='donor_detail'),
    path('donors/<int:pk>/edit/', DonorUpdateView.as_view(), name='donor_update'),
    path('donors/<int:pk>/delete/', DonorDeleteView.as_view(), name='donor_delete'),

    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/', recipient_detail, name='recipient_detail'),
    path('recipients/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

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

    path('auto-add-hla/', auto_add_hla, name='auto_add_hla'),
]