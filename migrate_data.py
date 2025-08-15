#!/usr/bin/env python
"""
Script pour migrer les données de Contact vers Affaire
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from clients.models import Client, Contact
from affaires.models import Affaire

def migrate_contacts_to_affaires():
    """Migre tous les contacts vers leurs affaires correspondantes"""
    print("=== Migration des contacts vers les affaires ===")
    
    with transaction.atomic():
        contacts_migres = 0
        
        for client in Client.objects.all():
            print(f"\nTraitement client: {client.entity_name}")
            
            # Récupérer les affaires et contacts du client
            affaires = client.affaires.all()
            contacts = client.contacts.filter(affaire__isnull=True)  # Contacts pas encore migrés
            
            if not affaires.exists():
                print(f"  ⚠️  Pas d'affaire - contacts conservés sur client uniquement")
                continue
                
            if not contacts.exists():
                print(f"  ✅ Tous les contacts déjà migrés")
                continue
                
            # Assigner tous les contacts à la première affaire
            premiere_affaire = affaires.first()
            print(f"  📝 Migration de {contacts.count()} contact(s) vers {premiere_affaire.affaire_number}")
            
            for contact in contacts:
                contact.affaire = premiere_affaire
                contact.save()
                contacts_migres += 1
                print(f"    ✅ {contact.nom} {contact.prenom}")
        
        print(f"\n=== Résumé ===")
        print(f"Total contacts migrés: {contacts_migres}")

if __name__ == "__main__":
    migrate_contacts_to_affaires()