from django import forms
from django.core.validators import MinValueValidator
from .models import Ecriture, Compte

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