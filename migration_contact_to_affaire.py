#!/usr/bin/env python
"""
Script de migration pour changer la relation Contact de Client vers Affaire
"""
import os
import sys
import django
from django.db import transaction

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionnaire_factures.settings')
django.setup()

from clients.models import Client, Contact
from affaires.models import Affaire


def migrate_contacts_to_affaires():
    """
    Migre les contacts existants de Client vers Affaire
    
    Stratégie :
    - Pour chaque client ayant des affaires, créer un contact principal par affaire
    - Si le client n'a qu'un contact principal, le dupliquer pour chaque affaire
    - Si le client a plusieurs contacts, distribuer selon la logique métier
    """
    print("=== Début de la migration Contact → Affaire ===")
    
    with transaction.atomic():
        # Statistiques avant migration
        total_clients = Client.objects.count()
        total_contacts = Contact.objects.count() 
        total_affaires = Affaire.objects.count()
        
        print(f"Avant migration:")
        print(f"  - Clients: {total_clients}")
        print(f"  - Contacts: {total_contacts}")
        print(f"  - Affaires: {total_affaires}")
        
        # Traitement client par client
        contacts_created = 0
        contacts_updated = 0
        
        for client in Client.objects.all():
            print(f"\nTraitement du client: {client.entity_name}")
            
            # Récupérer toutes les affaires du client
            affaires = client.affaires.all()
            
            if not affaires.exists():
                print(f"  ⚠️  Client sans affaire - contacts conservés sur client")
                continue
                
            # Récupérer les contacts du client
            contacts = client.contacts.all()
            contact_principal = client.contact_principal
            
            print(f"  - {affaires.count()} affaire(s)")
            print(f"  - {contacts.count()} contact(s)")
            
            if not contacts.exists():
                print(f"  ⚠️  Client sans contact")
                continue
                
            # Cas 1: Un seul contact principal -> le dupliquer pour chaque affaire
            if contacts.count() == 1 and contact_principal:
                for affaire in affaires:
                    if affaire == affaires.first():
                        # Première affaire: modifier le contact existant
                        print(f"    📝 Assignation contact principal à affaire {affaire.affaire_number}")
                        # Note: La modification du modèle se fera dans l'étape suivante
                        contacts_updated += 1
                    else:
                        # Autres affaires: créer un nouveau contact
                        print(f"    ➕ Création nouveau contact pour affaire {affaire.affaire_number}")
                        # Note: La création se fera après modification du modèle
                        contacts_created += 1
            
            # Cas 2: Plusieurs contacts -> répartir (pour l'instant, assigner tous à la première affaire)
            elif contacts.count() > 1:
                premiere_affaire = affaires.first()
                print(f"    📝 Assignation de {contacts.count()} contacts à la première affaire {premiere_affaire.affaire_number}")
                contacts_updated += contacts.count()
        
        print(f"\n=== Résumé de la migration planifiée ===")
        print(f"Contacts à modifier: {contacts_updated}")
        print(f"Contacts à créer: {contacts_created}")
        print(f"⚠️  Migration simulée - modèle non encore modifié")


def rollback_migration():
    """
    Fonction de rollback en cas de problème
    """
    print("=== Rollback disponible via restauration de db.sqlite3.backup_* ===")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("MODE DRY-RUN: Simulation de la migration")
        migrate_contacts_to_affaires()
    elif len(sys.argv) > 1 and sys.argv[1] == "--execute":
        print("EXÉCUTION RÉELLE: Migration en cours...")
        print("⚠️  Cette fonctionnalité sera activée après modification des modèles")
        # migrate_contacts_to_affaires()
    else:
        print("Usage:")
        print("  python migration_contact_to_affaire.py --dry-run   # Simulation")
        print("  python migration_contact_to_affaire.py --execute   # Exécution")