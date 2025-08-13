# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Environment Setup
```bash
# Install dependencies with pipenv
pipenv install

# Activate virtual environment
pipenv shell

# Install dev dependencies for testing and linting
pipenv install --dev
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run with auto-reload (django-browser-reload is configured)
python manage.py runserver
```

### Database Operations
```bash
# Make migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic
```

### Testing and Code Quality
```bash
# Run tests with pytest
pytest

# Run tests for specific app
pytest clients/

# Run flake8 linting
flake8

# Run Django's built-in tests
python manage.py test
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

## Architecture Overview

### Core Business Logic
This is a Django-based invoice management system with the following key models and relationships:

**Client ↔ Contact Relationship**: 
- `Client` has many `Contact`s (one-to-many)
- Each client can have multiple contacts, but only one marked as `is_principal=True`
- Contact model automatically ensures only one principal contact per client

**Client ↔ Affaire ↔ Invoice Chain**:
- `Client` → `Affaire` (business deals/projects) → `Invoice` (billing)
- This creates a hierarchical structure: Client manages multiple business deals, each deal can have multiple invoices

**Invoice ↔ Payment Tracking**:
- `Invoice` has many `Payment`s with automatic status updates
- Invoice status automatically calculated based on payment amounts vs. total due

### Model Relationships and Business Rules

**Client Model** (`clients/models.py:5-39`):
- Stores entity information with optional contact fields
- Property `total_affaire_client` calculates sum of all related Affaire budgets
- Property `contact_principal` gets the main contact

**Contact Model** (`clients/models.py:41-85`):
- Foreign key to Client with `is_principal` boolean flag
- Unique constraint ensures only one principal contact per client
- Auto-saves first contact as principal

**Affaire Model** (`affaires/models.py:7-45`):
- Links to Client, stores project budget and description
- Properties calculate `total_facture_ht` (billed amount) and `reste_a_facturer` (remaining to bill)
- Automatically copies client name on save

**Invoice Model** (`factures/models.py:6-84`):
- Links to both Affaire and Client with automatic client name copying
- Auto-calculates `amount_ttc` from `amount_ht` and `vat_rate`
- Method `update_statut()` automatically determines payment status
- Property `balance` shows remaining amount due

**Payment Model** (`factures/models.py:86-105`):
- Links to Invoice, automatically updates invoice status on save
- Triggers invoice status recalculation via `update_statut()`

### Authentication System
- Custom User model (`users/models.py:22-40`) using email as username
- Extends `AbstractBaseUser` and `PermissionsMixin`
- Custom manager (`users/models.py:5-20`) handles user creation

### URL Structure
```
/ - Dashboard (dashboard app)
/clients/ - Client management
/clients/contact/ - Contact management  
/factures/ - Invoice and payment management
/affaires/ - Business deal management
/admin/ - Django admin interface
```

### Template Architecture
- Base template (`templates/base.html`) with sidebar navigation
- App-specific template directories under `templates/pages/`
- Responsive design with custom CSS (`static/style.css`)

### Configuration
- Environment variables loaded via `django-environ` from `.env` file
- French locale (`LANGUAGE_CODE = 'fr-fr'`, `TIME_ZONE = 'Europe/Paris'`)
- SQLite for development, PostgreSQL support configured for production
- Custom user model: `AUTH_USER_MODEL = 'users.CustomUser'`

### Development Tools
- `django-browser-reload` for auto-refresh during development
- `reportlab` for PDF generation
- `pytest` and `pytest-django` for testing
- `flake8` for code linting

### Production Deployment
- Docker Compose setup with PostgreSQL, Nginx, and Gunicorn
- Static files served via Nginx
- Health checks configured for database