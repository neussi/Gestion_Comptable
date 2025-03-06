from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('comptes/', CompteListView.as_view(), name='compte_list'),
    path('comptes/<int:pk>/', CompteDetailView.as_view(), name='compte_detail'),
    path('comptes/nouveau/', CompteCreateView.as_view(), name='compte_create'),
    path('comptes/<int:pk>/modifier/', CompteUpdateView.as_view(), name='compte_update'),
    path('comptes/<int:pk>/supprimer/', CompteDeleteView.as_view(), name='compte_delete'),
    # URLs des écritures comptables
    path('ecritures/', EcritureListView.as_view(), name='ecriture_list'),
    path('ecritures/<int:pk>/', EcritureDetailView.as_view(), name='ecriture_detail'),
    path('ecritures/create/', EcritureCreateView.as_view(), name='ecriture_create'),
    path('ecritures/<int:pk>/update/', EcritureUpdateView.as_view(), name='ecriture_update'),
    path('ecritures/<int:pk>/delete/', EcritureDeleteView.as_view(), name='ecriture_delete'),
    path('ecritures/<int:pk>/upload/', upload_justificatif, name='upload_justificatif'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'), 
    
    path('fournisseurs/', FournisseurListView.as_view(), name='fournisseur_list'),
    path('fournisseurs/<int:pk>/', FournisseurDetailView.as_view(), name='fournisseur_detail'),
    path('fournisseurs/create/', FournisseurCreateView.as_view(), name='fournisseur_create'),
    path('fournisseurs/<int:pk>/update/', FournisseurUpdateView.as_view(), name='fournisseur_update'),
    path('fournisseurs/<int:pk>/delete/', FournisseurDeleteView.as_view(), name='fournisseur_delete'),

    path('factures/', FactureListView.as_view(), name='facture_list'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name='facture_detail'),
    path('factures/create/', FactureCreateView.as_view(), name='facture_create'),
    path('factures/<int:pk>/update/', FactureUpdateView.as_view(), name='facture_update'),
    path('factures/<int:pk>/delete/', FactureDeleteView.as_view(), name='facture_delete'),


    path('factures/', FactureListView.as_view(), name='facture_list'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name='facture_detail'),
    path('factures/create/', FactureCreateView.as_view(), name='facture_create'),
    path('factures/<int:pk>/update/', FactureUpdateView.as_view(), name='facture_update'),
    path('factures/<int:pk>/delete/', FactureDeleteView.as_view(), name='facture_delete'),
    path('factures/<int:pk>/envoyer/', envoyer_facture_email, name='envoyer_facture_email'),
    path('factures/<int:pk>/etat/<str:etat>/', changer_etat_facture, name='changer_etat_facture'),



    # path('logout/', logout_view, name='logout'),
]