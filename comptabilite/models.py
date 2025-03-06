from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class PlanComptable(models.Model):
    """Plan comptable - structure de comptes pour une entreprise"""
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Compte(models.Model):
    """Comptes dans le plan comptable"""
    TYPE_CHOICES = [
        ('Actif', 'Actif'),
        ('Passif', 'Passif'),
        ('Capitaux propres', 'Capitaux propres'),
    ]
    
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    numero = models.CharField(max_length=50, unique=True)
    solde = models.DecimalField(max_digits=18, decimal_places=2, default=0, 
                                validators=[MinValueValidator(0)])
    plan_comptable = models.ForeignKey(PlanComptable, on_delete=models.CASCADE, related_name='comptes')

    def __str__(self):
        return f"{self.numero} - {self.nom}"


class Ecriture(models.Model):
    """Écritures comptables (transactions)"""
    date = models.DateField()
    montant = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0.01)])
    commentaire = models.TextField(blank=True, null=True)
    justificatif = models.CharField(max_length=255, blank=True, null=True)
    debit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='ecritures_debit')
    credit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='ecritures_credit')

    def __str__(self):
        return f"Écriture {self.id} - {self.date} - {self.montant}€"
    
    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("La date ne peut pas être dans le futur")


class Client(models.Model):
    """Clients de l'entreprise"""
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    """Fournisseurs de l'entreprise"""
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nom


class Facture(models.Model):
    """Factures émises ou reçues"""
    ETAT_CHOICES = [
        ('Non payé', 'Non payé'),
        ('Partiellement payé', 'Partiellement payé'),
        ('Payé', 'Payé'),
    ]
    
    numero = models.CharField(max_length=50)
    date_emission = models.DateField()
    date_echeance = models.DateField()
    montant_total = models.DecimalField(max_digits=18, decimal_places=2, 
                                      validators=[MinValueValidator(0)])
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='factures')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, related_name='factures')

    def __str__(self):
        return f"Facture {self.numero} - {self.montant_total}€"
    
    def clean(self):
        if self.date_emission > timezone.now().date():
            raise ValidationError("La date d'émission ne peut pas être dans le futur")
        
        if self.date_echeance < self.date_emission:
            raise ValidationError("La date d'échéance doit être postérieure ou égale à la date d'émission")


class Tresorerie(models.Model):
    """Mouvements de trésorerie"""
    FLUX_CHOICES = [
        ('Entrée', 'Entrée'),
        ('Sortie', 'Sortie'),
    ]
    
    date = models.DateField()
    flux = models.CharField(max_length=50, choices=FLUX_CHOICES)
    montant = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.flux} de {self.montant}€ le {self.date}"
    
    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("La date ne peut pas être dans le futur")


class Immobilisation(models.Model):
    """Immobilisations et amortissements"""
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_acquisition = models.DateField()
    valeur_acquisition = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)])
    duree_de_vie = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    taux_amortissement = models.DecimalField(max_digits=5, decimal_places=4, 
                                           validators=[MinValueValidator(0), MaxValueValidator(1)])
    valeur_residuelle = models.DecimalField(max_digits=18, decimal_places=2, 
                                          validators=[MinValueValidator(0)], blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.valeur_acquisition}€"
    
    def clean(self):
        if self.date_acquisition > timezone.now().date():
            raise ValidationError("La date d'acquisition ne peut pas être dans le futur")
