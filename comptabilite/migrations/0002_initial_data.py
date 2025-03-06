# migrations/0002_initial_data.py

from django.db import migrations
from django.utils import timezone
import random
from datetime import timedelta

def load_initial_data(apps, schema_editor):
    PlanComptable = apps.get_model('comptabilite', 'PlanComptable')
    Compte = apps.get_model('comptabilite', 'Compte')
    Ecriture = apps.get_model('comptabilite', 'Ecriture')
    Client = apps.get_model('comptabilite', 'Client')
    Fournisseur = apps.get_model('comptabilite', 'Fournisseur')
    Facture = apps.get_model('comptabilite', 'Facture')
    Tresorerie = apps.get_model('comptabilite', 'Tresorerie')
    Immobilisation = apps.get_model('comptabilite', 'Immobilisation')
    
    # 1. Chargement des plans comptables
    plans_comptables = [
        {'nom': 'Plan Comptable Général', 'description': 'Plan comptable standard pour entreprises.'},
        {'nom': 'Plan Comptable Simplifié', 'description': 'Plan comptable pour les petites entreprises.'},
        {'nom': 'Plan Comptable Avancé', 'description': 'Plan comptable pour les grandes entreprises.'},
        {'nom': 'Plan Comptable Associatif', 'description': 'Plan comptable pour associations.'},
        {'nom': 'Plan Comptable Bancaire', 'description': 'Plan comptable spécifique au secteur bancaire.'},
    ]
    
    for plan_data in plans_comptables:
        PlanComptable.objects.create(**plan_data)
    
    # 2. Chargement des comptes initiaux
    comptes_initiaux = [
        {'nom': 'Caisse', 'type': 'Actif', 'numero': '1000', 'solde': 15000.00, 'plan_comptable_id': 1},
        {'nom': 'Banque', 'type': 'Actif', 'numero': '1001', 'solde': 50000.00, 'plan_comptable_id': 1},
        {'nom': 'Capital Social', 'type': 'Capitaux propres', 'numero': '3000', 'solde': 100000.00, 'plan_comptable_id': 1},
        {'nom': 'Dettes Fournisseurs', 'type': 'Passif', 'numero': '2000', 'solde': 25000.00, 'plan_comptable_id': 1},
        {'nom': 'Immobilisations Corporelles', 'type': 'Actif', 'numero': '4000', 'solde': 75000.00, 'plan_comptable_id': 1},
    ]
    
    for compte_data in comptes_initiaux:
        Compte.objects.create(**compte_data)
    
    # 3. Génération de 95 comptes supplémentaires
    types_compte = ['Actif', 'Passif', 'Capitaux propres']
    for i in range(6, 101):
        type_index = i % 3
        solde = round(random.random() * 10000, 2)
        Compte.objects.create(
            nom=f'Compte {i}',
            type=types_compte[type_index],
            numero=f'10{i}',
            solde=solde,
            plan_comptable_id=1
        )
    
    # 4. Chargement des écritures comptables
    comptes = list(Compte.objects.all())
    today = timezone.now().date()
    
    for i in range(1, 101):
        date = today - timedelta(days=i)
        montant = round(random.random() * 5000 + 100, 2)
        debit_id = (i % 20) + 1
        credit_id = ((i + 10) % 20) + 1
        
        # Éviter que debit_id et credit_id soient égaux
        if debit_id == credit_id:
            credit_id = (credit_id + 1) % len(comptes)
            if credit_id == 0:
                credit_id = 1
        
        Ecriture.objects.create(
            date=date,
            montant=montant,
            commentaire=f'Ecriture automatique {i}',
            debit_id=debit_id,
            credit_id=credit_id
        )
    
    # 5. Chargement des clients
    for i in range(1, 101):
        Client.objects.create(
            nom=f'Client {i}',
            adresse=f'Adresse {i}',
            email=f'client{i}@example.com',
            telephone=f'6{i}0000000'
        )
    
    # 6. Chargement des fournisseurs
    for i in range(1, 101):
        Fournisseur.objects.create(
            nom=f'Fournisseur {i}',
            adresse=f'Adresse {i}',
            email=f'fournisseur{i}@example.com',
            telephone=f'7{i}0000000'
        )
    
    # 7. Chargement des factures
    etats_facture = ['Non payé', 'Partiellement payé', 'Payé']
    for i in range(1, 101):
        etat_index = i % 3
        date_emission = today - timedelta(days=i)
        date_echeance = today + timedelta(days=(i % 10))
        montant = round(random.random() * 1000 + 500, 2)
        client_id = (i % 20) + 1
        fournisseur_id = ((i + 5) % 20) + 1
        
        Facture.objects.create(
            numero=f'F{i:03d}',
            date_emission=date_emission,
            date_echeance=date_echeance,
            montant_total=montant,
            etat=etats_facture[etat_index],
            client_id=client_id,
            fournisseur_id=fournisseur_id
        )
    
    # 8. Chargement des entrées de trésorerie
    flux_types = ['Entrée', 'Sortie']
    for i in range(1, 101):
        flux_index = i % 2
        date = today - timedelta(days=i)
        montant = round(random.random() * 3000 + 500, 2)
        
        Tresorerie.objects.create(
            date=date,
            flux=flux_types[flux_index],
            montant=montant,
            description=f'Transaction {i}'
        )
    
    # 9. Chargement des immobilisations
    for i in range(1, 101):
        date_acquisition = today - timedelta(days=i * 30)
        valeur_acquisition = round(random.random() * 10000 + 1000, 2)
        duree_de_vie = (i % 10) + 1
        taux_amortissement = round(random.random(), 4)
        valeur_residuelle = round(random.random() * 500, 2)
        
        Immobilisation.objects.create(
            nom=f'Immobilisation {i}',
            description=f'Description de l\'immobilisation {i}',
            date_acquisition=date_acquisition,
            valeur_acquisition=valeur_acquisition,
            duree_de_vie=duree_de_vie,
            taux_amortissement=taux_amortissement,
            valeur_residuelle=valeur_residuelle
        )

def reverse_func(apps, schema_editor):
    PlanComptable = apps.get_model('comptabilite', 'PlanComptable')
    Compte = apps.get_model('comptabilite', 'Compte')
    Ecriture = apps.get_model('comptabilite', 'Ecriture')
    Client = apps.get_model('comptabilite', 'Client')
    Fournisseur = apps.get_model('comptabilite', 'Fournisseur')
    Facture = apps.get_model('comptabilite', 'Facture')
    Tresorerie = apps.get_model('comptabilite', 'Tresorerie')
    Immobilisation = apps.get_model('comptabilite', 'Immobilisation')
    
    # Supprimer toutes les données
    Immobilisation.objects.all().delete()
    Tresorerie.objects.all().delete()
    Facture.objects.all().delete()
    Client.objects.all().delete()
    Fournisseur.objects.all().delete()
    Ecriture.objects.all().delete()
    Compte.objects.all().delete()
    PlanComptable.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('comptabilite', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(load_initial_data, reverse_func),
    ]