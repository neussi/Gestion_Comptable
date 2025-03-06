
# 📊 Gestion Comptable

[![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/neussi/Gestion_Comptable)

## 📌 Description

**Gestion Comptable** est une application web développée avec Django pour faciliter la gestion comptable des entreprises de toutes tailles. Elle permet de gérer les comptes, saisir les écritures comptables, générer des factures, suivre la trésorerie et produire des rapports financiers détaillés.

## 🚀 Fonctionnalités Principales

- 📂 **Gestion des comptes** : Création et suivi des comptes comptables (actifs, passifs, capitaux, etc.).
- 📝 **Saisie des écritures comptables** : Ajout manuel ou automatique des écritures avec pièces justificatives.
- 🏢 **Gestion des clients et fournisseurs** : Suivi des transactions, relances et rapports d’encours.
- 🧾 **Facturation et gestion des recettes** : Génération et envoi de factures personnalisées.
- 💰 **Suivi de la trésorerie** : Visualisation des flux financiers et rapprochement bancaire.
- 🏠 **Gestion des immobilisations** : Suivi des équipements avec calcul des amortissements.
- 📊 **Génération de rapports financiers** : Bilan, compte de résultat, export en PDF ou Excel.
- 🔐 **Gestion des utilisateurs** : Rôles admin, comptable et utilisateur standard avec accès restreint.

## 🛠️ Environnement Technique

### 🔹 Backend
- **Langage** : Python
- **Framework** : Django 4.x
- **Base de données** : SQLite
- **Authentification** : Système d’authentification intégré de Django

### 🔹 Frontend
- **HTML5, CSS3, JavaScript (JQuery)**
- **Framework CSS** : Bootstrap pour un design responsive

### 🔹 Déploiement
- **Serveur de développement** : Intégré à Django
- **Déploiement en production** : Gunicorn ou Apache

## 📦 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/neussi/Gestion_Comptable.git
   cd Gestion_Comptable
   ```
2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv env
   source env/bin/activate  # Pour macOS/Linux
   env\Scripts\activate  # Pour Windows
   ```
3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```
5. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```
6. **Accéder à l’application**
   - Ouvrir un navigateur et aller sur : `http://127.0.0.1:8000/`

## 🏗️ Structure du Projet

```
Gestion_Comptable/
│── comptabilite/         # Répertoire principal du projet Django
│   ├── templates/             # Fichiers HTML
│   ├── static/                # Fichiers CSS, JS, images
│   ├── models.py              # Définition des modèles
|   |── forms.py               # Définition des formulaires
│   ├── views.py               # Logique des vues
│   ├── urls.py                # Routage des URLs
│── db.sqlite3                 # Base de données SQLite
│── manage.py                  # Commande de gestion Django
│── requirements.txt           # Dépendances du projet
│── README.md                  # Documentation du projet
```

## 📜 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l’utiliser et de le modifier selon vos besoins.

## 📩 Contact

Développé par **Neussi Patrice**  
📧 Email : [patriceneussi9@gmail.com](mailto:patriceneussi9@gmail.com)  
🔗 GitHub : [Neussi Patrice](https://github.com/neussi)

---

✨ *Contribuez au projet en signalant des bugs ou en proposant des améliorations sur GitHub !* 🚀
