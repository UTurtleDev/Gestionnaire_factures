FROM python:3.12-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings


# Définir le répertoire de travail
WORKDIR /app


# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc postgresql-client libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer pipenv
RUN pip install --upgrade pip \
    && pip install pipenv

# Copier les fichiers Pipfile et Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Installer les dépendances
RUN pipenv install --deploy --system

# Copier le projet
COPY . .

# Créer un utilisateur non-root
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Commande pour démarrer Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

