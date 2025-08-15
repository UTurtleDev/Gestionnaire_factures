#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from clients.models import Contact

contacts_sans_affaire = Contact.objects.filter(affaire__isnull=True)
print(f"Contacts sans affaire: {contacts_sans_affaire.count()}")

for contact in contacts_sans_affaire:
    print(f"- {contact.nom} {contact.prenom} (client: {contact.client})")