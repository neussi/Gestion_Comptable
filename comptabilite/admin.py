# admin.py
from django.contrib import admin
from .models import (
    PlanComptable, Compte, Ecriture, Client, 
    Fournisseur, Facture, Tresorerie, Immobilisation
)

@admin.register(PlanComptable)
class PlanComptableAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'description')
    search_fields = ('nom',)

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'nom', 'type', 'solde', 'plan_comptable')
    list_filter = ('type', 'plan_comptable')
    search_fields = ('nom', 'numero')

@admin.register(Ecriture)
class EcritureAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'montant', 'debit', 'credit', 'commentaire')
    list_filter = ('date',)
    search_fields = ('commentaire',)
    date_hierarchy = 'date'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'email', 'telephone')
    search_fields = ('nom', 'email')

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'email', 'telephone')
    search_fields = ('nom', 'email')

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'date_emission', 'date_echeance', 
                    'montant_total', 'etat', 'client', 'fournisseur')
    list_filter = ('etat', 'date_emission')
    search_fields = ('numero',)
    date_hierarchy = 'date_emission'

@admin.register(Tresorerie)
class TresorerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'flux', 'montant', 'description')
    list_filter = ('flux', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Immobilisation)
class ImmobilisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date_acquisition', 'valeur_acquisition', 
                    'duree_de_vie', 'taux_amortissement', 'valeur_residuelle')
    search_fields = ('nom',)
    date_hierarchy = 'date_acquisition'