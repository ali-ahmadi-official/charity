from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    main,
    DonorListView, DonorCreateView, donor_detail, DonorUpdateView, DonorDeleteView,
    RecipientListView, RecipientCreateView, recipient_detail, RecipientUpdateView, RecipientDeleteView
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
]