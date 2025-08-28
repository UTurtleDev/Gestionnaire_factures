# 📊 Gestionnaire de Factures 💼

![Badge Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white)
![Badge Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Badge Pipenv](https://img.shields.io/badge/Pipenv-Gestion_Dépendances-orange?style=for-the-badge&logo=python&logoColor=white)

## 🌟 Présentation

**Gestionnaire de Factures** est une application web développée avec Django qui permet de gérer simplement et efficacement les clients, factures, affaires et règlements d'une entreprise. Cette interface intuitive est conçue pour faciliter le suivi financier et la relation client avec une architecture robuste Client → Affaire → Facture.

## ✨ Fonctionnalités

### 👥 Gestion des clients et contacts
- ✅ Création, consultation, modification et suppression de clients
- ✅ Gestion des contacts associés avec contact principal
- ✅ Stockage des informations essentielles (nom, adresse, coordonnées)
- ✅ Calcul automatique du total des affaires par client

### 📁 Gestion des affaires
- ✅ Création et suivi
 des projets/budgets par client
- ✅ Numérotation unique des affaires avec description
- ✅ Calcul automatique du taux d'avancement (facturé/budget)
- ✅ Création d'un facture à partir de l'affaire
- ✅ Suivi du montant restant à facturer par affaire

### 💰 Gestion des factures
- ✅ Création de factures (facture, avoir) liées aux affaires
- ✅ Calcul automatique du montant TTC avec taux de TVA personnalisable
- ✅ Gestion des statuts de paiement (à payer, payée, en retard...)
- ✅ Upload et stockage des PDF de factures
- ✅ Mise à jour automatique du statut selon les règlements

### 💳 Gestion des règlements
- ✅ Enregistrement des paiements avec différents moyens de paiement
- ✅ Mise à jour automatique du statut des factures
- ✅ Historique complet des paiements avec balance restante

### 📊 Tableau de bord et analytics
- ✅ Vue d'ensemble avec métriques clés
- ✅ Top clients par chiffre d'affaires
- ✅ Graphiques de revenus avec Matplotlib
- ✅ Affaires en cours et totaux par client
- ✅ Interface utilisateur moderne et réactive

### 📤 Export et sauvegarde
- ✅ Export CSV/Excel des clients, factures et règlements
- ✅ Export complet de la base de données SQLite
- ✅ Filtrage par dates pour les exports

### 🔍 Fonctionnalités avancées
- ✅ Recherche globale dans l'application
- ✅ Système d'authentification personnalisé (email)
<!-- - ✅ Pagination et tri des listes -->
- ✅ Validation automatique des montants (avoirs négatifs)
- ✅ Interface en français avec formatage européen des montants

## 🛠️ Technologies

- **Backend**: Django 5.2, Python 3.12
- **Frontend**: HTML, CSS (interface responsive)
- **Base de données**: SQLite (développement), PostgreSQL (production)
- **Gestion des dépendances**: Pipenv
- **Graphiques**: Matplotlib, NumPy
- **Export**: OpenPyXL, ReportLab


## 🚀 Installation

### Développement local

```bash
# Cloner le dépôt
git clone https://github.com/votre-nom/gestionnaire-factures.git
cd gestionnaire-factures

# Installer les dépendances avec pipenv
pipenv install

# Activer l'environnement virtuel
pipenv shell

# Effectuer les migrations
python manage.py migrate

# Créer un super utilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```


## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre-clé-secrète-très-longue-et-sécurisée
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Base de données PostgreSQL (pour production)
DATABASE_URL=postgresql://user:password@db:5432/dbname
POSTGRES_DB=gestfacts
POSTGRES_USER=postgres
POSTGRES_PASSWORD=motdepasse
```

## 📝 Structure du projet

```
Gestionnaire_factures/
│
├── 📁 affaires/           # Gestion des projets/affaires
├── 📁 clients/            # Gestion des clients et contacts
├── 📁 config/             # Configuration Django principale
├── 📁 dashboard/          # Tableau de bord et analytics
├── 📁 factures/           # Gestion des factures et règlements
├── 📁 nginx/              # Configuration Nginx pour Docker
├── 📁 static/             # Fichiers statiques (CSS, images)
├── 📁 templates/          # Templates HTML
├── 📁 users/              # Système d'authentification personnalisé
├── 📁 utils/              # Utilitaires (exports, graphiques)
│
l'application
├── 📦 Pipfile             # Dépendances du projet
├── 📦 Pipfile.lock        # Versions verrouillées
├── 📄 requirements.txt    # Dépendances pour production
└── ⚙️ manage.py           # Script de gestion Django
```

## 🏗️ Architecture

### Modèles et relations
- **Client** ↔ **Contact** (un-à-plusieurs avec contact principal)
- **Client** → **Affaire** → **Facture** (hiérarchie des données)
- **Facture** ↔ **Paiement** (suivi automatique des règlements)

### URLs principales
- `/` - Tableau de bord principal
- `/clients/` - Gestion des clients
- `/affaires/` - Gestion des affaires
- `/factures/` - Factures et règlements
- `/admin/` - Interface d'administration Django

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).

---

🚀 **Développé avec Django** 

*Application de gestion de facturation moderne avec interface responsive et analytics avancés*