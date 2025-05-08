# 📊 Gestionnaire de Factures 💼

![Badge Django](https://img.shields.io/badge/Django-5.1-green?style=for-the-badge&logo=django&logoColor=white)
![Badge Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Badge Pipenv](https://img.shields.io/badge/Pipenv-Gestion_Dépendances-orange?style=for-the-badge&logo=python&logoColor=white)

## 🌟 Présentation

**Gestionnaire de Factures** est une application web développée avec Django qui permet de gérer simplement et efficacement les clients, factures, affaires et règlements d'une entreprise. Cette interface intuitive est conçue pour faciliter le suivi financier et la relation client.

## ✨ Fonctionnalités

### 👥 Gestion des clients
- ✅ Création, consultation, modification et suppression de clients
- ✅ Stockage des informations essentielles (nom, adresse, coordonnées)
- ✅ Interface conviviale pour naviguer entre les clients

### 💰 Gestion des factures
- ✅ Création de factures avec calcul automatique du montant TTC
- ✅ Suivi du statut des paiements (payée, partiellement payée, en retard...)
- ✅ Association des factures aux clients et aux affaires
- ✅ Vue détaillée de chaque facture

### 📁 Gestion des affaires
- ✅ Suivi des projets et budgets associés
- ✅ Liaison entre affaires, clients et factures
- ✅ Vue d'ensemble des montants facturés par projet

### 💳 Gestion des paiements
- ✅ Enregistrement des règlements
- ✅ Mise à jour automatique du statut des factures
- ✅ Historique complet des paiements

### 📊 Tableau de bord
- ✅ Vue d'ensemble de l'activité
- ✅ Interface utilisateur moderne et réactive

## 🛠️ Technologies

- **Backend**: Django 5.1, Python 3.10+
- **Frontend**: HTML, CSS (interface responsive)
- **Base de données**: SQLite (par défaut), adaptable à PostgreSQL
- **Gestion des dépendances**: Pipenv

## 🚀 Installation

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

# Créer un super utilisateur (facultatif)
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

## 🔧 Configuration

1. Créer un fichier `.env` à la racine du projet avec les informations suivantes:

```
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📷 Captures d'écran

*Insérer des captures d'écran de l'application ici*

## 📝 Structure du projet

```
Gestionnaire_factures/
│
├── affaires/        # Gestion des projets/affaires
├── clients/         # Gestion des clients
├── config/          # Configuration Django
├── dashboard/       # Page d'accueil et tableau de bord
├── factures/        # Gestion des factures et règlements
├── static/          # Fichiers statiques (CSS, images)
├── templates/       # Templates HTML
├── users/           # Gestion des utilisateurs
│
├── Pipfile          # Dépendances du projet
├── Pipfile.lock     # Versions verrouillées des dépendances
└── manage.py        # Script de gestion Django
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).

---

Développé avec ❤️ par UTurtle