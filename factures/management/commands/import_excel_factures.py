import pandas as pd
from django.core.management.base import BaseCommand
from clients.models import Client
from affaires.models import Affaire
from factures.models import Invoice
from decimal import Decimal
from datetime import datetime

class Command(BaseCommand):
    help = 'Importe les factures depuis un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Chemin vers le fichier Excel')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Lire le fichier Excel
        df = pd.read_excel(excel_file)
        
        # Nettoyer les colonnes (enlever les espaces)
        df.columns = df.columns.str.strip()
        
        self.stdout.write("Début de l'importation...")
        
        for index, row in df.iterrows():
            try:
                # 1. Créer ou récupérer le client
                client_name = str(row['CLIENT']).strip()
                client, created = Client.objects.get_or_create(
                    entity_name=client_name,
                    defaults={'entity_name': client_name}
                )
                if created:
                    self.stdout.write(f"Client créé: {client_name}")
                
                # 2. Créer ou récupérer l'affaire
                affaire_number = str(row['N° Affaire']).strip()
                affaire_desc = str(row['Designation affaire']).strip()
                
                # Estimer le budget basé sur le montant de la facture (à ajuster)
                montant_ht = 0.00 # Montant à ajuster manuellement après import
                
                affaire, created = Affaire.objects.get_or_create(
                    affaire_number=affaire_number,
                    defaults={
                        'client': client,
                        'affaire_description': affaire_desc,
                        'budget': montant_ht  # À ajuster selon tes besoins
                    }
                )
                if created:
                    self.stdout.write(f"Affaire créée: {affaire_number}")
                
                # 3. Créer la facture
                invoice_number = str(row['N° facture']).strip()
                invoice_type = str(row['Type']).strip()
                
                # Nettoyer les montants
                amount_ht = self.clean_currency(row['Montant HT'])
                amount_tva = self.clean_currency(row['Montant TVA'])
                # amount_ttc = self.clean_currency(row['Montant TTC'])  # Non necessaire, calculé automatiquement mais pourrait servir par la suite
                
                # Calculer le taux de TVA
                # if amount_ht > 0:
                #     vat_rate = (amount_tva / amount_ht) * 100
                # else:
                #     vat_rate = 20.0  # Taux par défaut
                vat_rate = Decimal('20.0')  # Taux par défaut
                
                # Dates : conversion et nettoyage de la date excel en date python pour être reconnu par le model
                date_facture = self.parse_date(row['Date Facture'])
                date_encaissement = self.parse_date(row['Date encaissement'])
                
                # Créer la facture
                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    affaire=affaire,
                    client=client,
                    type=invoice_type,
                    amount_ht=amount_ht,
                    vat_rate=vat_rate,
                    date=date_facture,
                )
                
                self.stdout.write(f"Facture créée: {invoice_number}")
                
                # 4. Créer le paiement si encaissement
                if date_encaissement and not pd.isna(row['Montant encaissé €TTC']):
                    from factures.models import Payment
                    montant_encaisse = self.clean_currency(row['Montant encaissé €TTC'])
                    
                    Payment.objects.create(
                        invoice=invoice,
                        amount=montant_encaisse,
                        date=date_encaissement,
                        payment_method='VRT'  # Virement par défaut comme demandé
                    )
                    self.stdout.write(f"Paiement créé pour {invoice_number}")
                    
                    # 🔍 Debug
                    invoice.refresh_from_db()  # Recharge depuis la DB
                    self.stdout.write(f"Statut après paiement: {invoice.statut}")
                    self.stdout.write(f"Balance restante: {invoice.balance}")

                
            except Exception as e:
                self.stdout.write(f"Erreur ligne {index + 1}: {str(e)}")
                continue
        
        self.stdout.write(self.style.SUCCESS("Importation terminée !"))

        # 🔍 Debug
        invoice.refresh_from_db()  # Recharge depuis la DB
        self.stdout.write(f"Statut après paiement: {invoice.statut}")
        self.stdout.write(f"Balance restante: {invoice.balance}")
    
    def clean_currency(self, value):
        """Nettoie une valeur monétaire et la convertit en Decimal"""
        if pd.isna(value):
            return Decimal('0')
        
        # Enlever les espaces, € et remplacer virgule par point
        cleaned = str(value).replace('€', '').replace(' ', '').replace(',', '.')
        
        try:
            return Decimal(cleaned)
        except:
            return Decimal('0')
    
    def parse_date(self, date_value):
        """Parse une date depuis Excel"""
        if pd.isna(date_value):
            return None
        
        if isinstance(date_value, str):
            try:
                # Format DD/MM/YYYY
                return datetime.strptime(date_value, '%d/%m/%Y').date()
            except:
                return None
        
        # Si c'est déjà un datetime
        if hasattr(date_value, 'date'):
            return date_value.date()
        
        return None