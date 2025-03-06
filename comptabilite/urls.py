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


    # path('logout/', logout_view, name='logout'),
]