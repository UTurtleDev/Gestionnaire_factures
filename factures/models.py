from django.db import models
from datetime import datetime, timedelta

# Create your models here.

class Invoice(models.Model):
    TYPE_CHOICES = [
        ('facture', 'Facture'),
        ('avoir', 'Avoir'),
        ('proforma', 'Proforma'),
        ]

    STATUT_CHOICES = [
        ('a_payer', 'À payer'),
        ('partiellement_payee', 'Partiellement payée'),
        ('payee', 'Payée'),
        ('en_retard', 'En retard'),
        ('annulee', 'Annulée'),
    ]

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='facture')
    affaire = models.ForeignKey('affaires.Affaire', on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=10, unique=True, db_index=True)
    client = models.ForeignKey('clients.Client', on_delete=models.SET_NULL, related_name='invoices', db_index=True, null=True)
    client_entity_name = models.CharField(max_length=100, blank=True, null=True)
    invoice_object = models.TextField(max_length=200)
    amount_ht = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_payer')

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
    def __str__(self):
        client_name = self.client_entity_name if self.client is None else self.client.entity_name
        return self.invoice_number

    
    def formatted_amount_ht(self):
        return f"{self.amount_ht:,.2f} €".replace(",", " ").replace(".", ",")
    
    @property
    def amount_ttc(self):
        return self.amount_ht * (1 + self.vat_rate / 100)
    
    def formatted_amount_ttc(self):
        return f"{self.amount_ttc:,.2f} €".replace(",", " ").replace(".", ",")
    
    @property
    def due_date(self):
        return self.date + timedelta(days=30)
    
    @property
    def balance(self):
        payments = self.payments.all()
        total_payments = sum(payment.amount for payment in payments)
        return self.amount_ttc - total_payments
    

    def update_statut(self):
        total_payments = sum(payment.amount for payment in self.payments.all())        
        if total_payments >= self.amount_ttc:
            self.statut = 'payee'
        elif total_payments > 0:
            self.statut = 'partiellement_payee'
        elif self.due_date < datetime.date.today():
            self.statut = 'en_retard'
        else:
            self.statut = 'a_payer'

        self.save()

    def save(self, *args, **kwargs):
        # Si le client existe, copie son nom dans client_entity_name
        if self.client:
            self.client_entity_name = self.client.entity_name
        super().save(*args, **kwargs)

    

class Payment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"


    def __str__(self):
        return f"Paiement de {self.amount}€ pour la facture {self.invoice.invoice_number}"
    
    def formatted_amount(self):
        return f"{self.amount:,.2f} €".replace(",", " ").replace(".", ",")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_statut()

# class Comment(models.Model):
#     invoice_number = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='comments')
#     date = models.DateTimeField(auto_now_add=True)
#     content = models.TextField(max_length=200)
#     author = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"Commentaire du {self.date.strftime('%d/%m/%Y')}"
    