
from .models import (
    Compte, Facture, Tresorerie, Ecriture, 
    Client, Fournisseur, PlanComptable, Immobilisation
)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Compte
from .forms import CompteForm
# def logout_view(request):
#     logout(request)
#     return redirect('login')

def dashboard(request):
    # Statistiques générales
    total_comptes = Compte.objects.count()
    total_clients = Client.objects.count()
    total_fournisseurs = Fournisseur.objects.count()

    # Calcul du chiffre d'affaires 
    chiffre_affaires = Ecriture.objects.filter(
        credit__type='Revenu'
    ).aggregate(total=Sum('montant'))['total'] or 0

    # Factures détaillées
    factures_impayees = Facture.objects.filter(
        etat__in=['Non payé', 'Partiellement payé']
    )
    total_factures_impayees = factures_impayees.count()
    montant_total_impaye = factures_impayees.aggregate(
        total=Sum('montant_total')
    )['total'] or 0

    # Trésorerie détaillée
    entrees_tresorerie = Tresorerie.objects.filter(flux='Entrée').aggregate(
        total=Sum('montant')
    )['total'] or 0
    sorties_tresorerie = Tresorerie.objects.filter(flux='Sortie').aggregate(
        total=Sum('montant')
    )['total'] or 0
    solde_tresorerie = entrees_tresorerie - sorties_tresorerie

    # Données récentes
    dernieres_activites = Ecriture.objects.select_related(
        'debit', 'credit'
    ).order_by('-date')[:10]

    # Immobilisations
    immobilisations_stats = {
        'total': Immobilisation.objects.count(),
        'valeur_totale': Immobilisation.objects.aggregate(
            total=Sum('valeur_acquisition')
        )['total'] or 0,
        'valeur_moyenne': Immobilisation.objects.aggregate(
            moyenne=Avg('valeur_acquisition')
        )['moyenne'] or 0
    }

    # Analyse des comptes par type
    repartition_comptes = Compte.objects.values('type').annotate(
        nombre=Count('id'), 
        solde_total=Sum('solde')
    )

    # Flux de trésorerie mensuels
    flux_tresorerie = Tresorerie.objects.filter(
        date__gte=timezone.now().date() - timedelta(days=180)
    ).annotate(
        mois=TruncMonth('date')
    ).values('mois').annotate(
        entrees=Sum('montant', filter=Q(flux='Entrée')),
        sorties=Sum('montant', filter=Q(flux='Sortie'))
    ).order_by('mois')

    # Statistiques des factures
    stats_factures = {
        'total': Facture.objects.count(),
        'payees': Facture.objects.filter(etat='Payé').count(),
        'partiellement_payees': Facture.objects.filter(etat='Partiellement payé').count(),
        'montant_total': Facture.objects.aggregate(total=Sum('montant_total'))['total'] or 0
    }

    context = {
        'statistiques_generales': {
            'total_comptes': total_comptes,
            'total_clients': total_clients,
            'total_fournisseurs': total_fournisseurs
        },
        'chiffre_affaires': round(chiffre_affaires, 2),
        'factures': {
            'total_impayees': total_factures_impayees,
            'montant_total_impaye': round(montant_total_impaye, 2),
            'stats': stats_factures
        },
        'tresorerie': {
            'entrees': round(entrees_tresorerie, 2),
            'sorties': round(sorties_tresorerie, 2),
            'solde_actuel': round(solde_tresorerie, 2)
        },
        'dernieres_activites': dernieres_activites,
        'immobilisations': immobilisations_stats,
        'repartition_comptes': list(repartition_comptes),
        'flux_tresorerie': list(flux_tresorerie),
        'user': request.user
    }

    return render(request, 'index.html', context)


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from .models import Compte, Ecriture
from .forms import CompteForm

# Liste des comptes comptables
class CompteListView(ListView):
    model = Compte
    template_name = 'compte_list.html'
    context_object_name = 'comptes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques par type de compte
        context['total_actifs'] = Compte.objects.filter(type='Actif').count()
        context['total_passifs'] = Compte.objects.filter(type='Passif').count()
        context['total_capitaux_propres'] = Compte.objects.filter(type='Capitaux propres').count()
        
        # Calcul des totaux
        context['solde_actifs'] = Compte.objects.filter(type='Actif').aggregate(Sum('solde'))['solde__sum'] or 0
        context['solde_passifs'] = Compte.objects.filter(type='Passif').aggregate(Sum('solde'))['solde__sum'] or 0
        context['solde_capitaux'] = Compte.objects.filter(type='Capitaux propres').aggregate(Sum('solde'))['solde__sum'] or 0
        
        return context

# Détail d'un compte comptable
class CompteDetailView(DetailView):
    model = Compte
    template_name = 'compte_detail.html'
    context_object_name = 'compte'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compte = self.get_object()
        
        # Récupérer les dernières écritures pour ce compte
        context['ecritures_debit'] = compte.ecritures_debit.all().order_by('-date')[:10]
        context['ecritures_credit'] = compte.ecritures_credit.all().order_by('-date')[:10]
        
        # Calculer le total des écritures
        total_debit = compte.ecritures_debit.aggregate(Sum('montant'))['montant__sum'] or 0
        total_credit = compte.ecritures_credit.aggregate(Sum('montant'))['montant__sum'] or 0
        
        context['total_debit'] = total_debit
        context['total_credit'] = total_credit
        context['solde_calcule'] = total_debit - total_credit
        
        return context

# Création d'un compte comptable
class CompteCreateView(CreateView):
    model = Compte
    form_class = CompteForm
    template_name = 'compte_form.html'
    success_url = reverse_lazy('compte_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = 'Création d\'un compte comptable'
        context['submit_text'] = 'Créer'
        context['action'] = 'create'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"Le compte {form.instance.nom} a été créé avec succès.")
        return super().form_valid(form)

# Modification d'un compte comptable
class CompteUpdateView(UpdateView):
    model = Compte
    form_class = CompteForm
    template_name = 'compte_form.html'
    success_url = reverse_lazy('compte_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = 'Modification d\'un compte comptable'
        context['submit_text'] = 'Enregistrer'
        context['action'] = 'update'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"Le compte {form.instance.nom} a été modifié avec succès.")
        return super().form_valid(form)

# Suppression d'un compte comptable
class CompteDeleteView(DeleteView):
    model = Compte
    template_name = 'compte_confirm_delete.html'
    success_url = reverse_lazy('compte_list')
    context_object_name = 'compte'
    
    def delete(self, request, *args, **kwargs):
        compte = self.get_object()
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f"Le compte {compte.nom} a été supprimé avec succès.")
        return result
    
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Ecriture, Compte
from .forms import EcritureForm

# Liste des écritures comptables
class EcritureListView(ListView):
    model = Ecriture
    template_name = 'ecriture_list.html'
    context_object_name = 'ecritures'
    ordering = ['-date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques des écritures
        context['total_ecritures'] = Ecriture.objects.count()
        context['total_debit'] = Ecriture.objects.aggregate(Sum('montant'))['montant__sum'] or 0
        context['total_credit'] = context['total_debit']  # Dans un système à double entrée, le total des débits = total des crédits
        
        # Statistiques des derniers mois
        from datetime import datetime, timedelta
        date_limite = datetime.now().date() - timedelta(days=30)
        context['ecritures_mois'] = Ecriture.objects.filter(date__gte=date_limite).count()
        context['montant_mois'] = Ecriture.objects.filter(date__gte=date_limite).aggregate(Sum('montant'))['montant__sum'] or 0
        
        return context

# Détail d'une écriture comptable
class EcritureDetailView(DetailView):
    model = Ecriture
    template_name = 'ecriture_detail.html'
    context_object_name = 'ecriture'

# Création d'une écriture comptable
class EcritureCreateView(CreateView):
    model = Ecriture
    form_class = EcritureForm
    template_name = 'ecriture_form.html'
    success_url = reverse_lazy('ecriture_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = 'Saisie d\'une écriture comptable'
        context['submit_text'] = 'Enregistrer'
        context['action'] = 'create'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"L'écriture comptable a été enregistrée avec succès.")
        return super().form_valid(form)

# Modification d'une écriture comptable
class EcritureUpdateView(UpdateView):
    model = Ecriture
    form_class = EcritureForm
    template_name = 'ecriture_form.html'
    success_url = reverse_lazy('ecriture_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = 'Modification d\'une écriture comptable'
        context['submit_text'] = 'Enregistrer les modifications'
        context['action'] = 'update'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"L'écriture comptable a été modifiée avec succès.")
        return super().form_valid(form)

# Suppression d'une écriture comptable
class EcritureDeleteView(DeleteView):
    model = Ecriture
    template_name = 'ecriture_confirm_delete.html'
    success_url = reverse_lazy('ecriture_list')
    context_object_name = 'ecriture'
    
    def delete(self, request, *args, **kwargs):
        ecriture = self.get_object()
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f"L'écriture comptable du {ecriture.date} a été supprimée avec succès.")
        return result

# Vue pour les pièces justificatives
def upload_justificatif(request, pk):
    ecriture = Ecriture.objects.get(pk=pk)
    if request.method == 'POST' and request.FILES.get('justificatif'):
        file = request.FILES['justificatif']
        # Gérer l'enregistrement du fichier
        ecriture.justificatif = file.name
        ecriture.save()
        messages.success(request, "Pièce justificative ajoutée avec succès.")
        return redirect('ecriture_detail', pk=pk)
    return render(request, 'upload_justificatif.html', {'ecriture': ecriture})    