from django import forms
from django.core.validators import MinValueValidator
from .models import Ecriture, Compte, Client, Fournisseur, Facture
from django.utils import timezone
class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['nom', 'type', 'numero', 'solde', 'plan_comptable']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}),
            'numero': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}),
            'solde': forms.NumberInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white', 'min': '0'}),
            'plan_comptable': forms.Select(attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des libellés (labels) explicites
        self.fields['nom'].label = "Nom du compte"
        self.fields['type'].label = "Type de compte"
        self.fields['numero'].label = "Numéro de compte"
        self.fields['solde'].label = "Solde initial"
        self.fields['plan_comptable'].label = "Plan comptable"
        
        # Ajouter des descriptions d'aide
        self.fields['numero'].help_text = "Exemple: 401 pour Fournisseurs"
        self.fields['solde'].help_text = "Montant en euros (€)"


class EcritureForm(forms.ModelForm):
    class Meta:
        model = Ecriture
        fields = ['date', 'montant', 'debit', 'credit', 'commentaire', 'justificatif']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'debit': forms.Select(attrs={'class': 'form-control'}),
            'credit': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'justificatif': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'adresse', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-800 border border-gray-700 rounded'}),
            'adresse': forms.Textarea(attrs={'class': 'w-full p-2 bg-gray-800 border border-gray-700 rounded', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 bg-gray-800 border border-gray-700 rounded'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-800 border border-gray-700 rounded'}),
        }


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 mb-3'}),
            'adresse': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 mb-3', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 mb-3'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 mb-3'}),
        }    



class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'date_emission', 'date_echeance', 'montant_total', 'etat', 'client', 'fournisseur']
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser avec la date du jour pour une nouvelle facture
        if not kwargs.get('instance'):
            self.fields['date_emission'].initial = timezone.now().date()
            self.fields['date_echeance'].initial = timezone.now().date() + timezone.timedelta(days=30)
        
        # Rendre les champs client et fournisseur mutuellement exclusifs
        self.fields['client'].required = False
        self.fields['fournisseur'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        fournisseur = cleaned_data.get('fournisseur')
        
        # Au moins un client ou un fournisseur doit être renseigné
        if not client and not fournisseur:
            raise forms.ValidationError("Vous devez sélectionner soit un client, soit un fournisseur.")
        
        # Mais pas les deux à la fois
        if client and fournisseur:
            raise forms.ValidationError("Vous ne pouvez pas sélectionner à la fois un client et un fournisseur.")
        
        return cleaned_data            