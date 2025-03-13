from django.db import models
from datetime import datetime, timedelta  

# Create your models here.

class Invoice(models.Model):
    TYPE_CHOICES = [
        ('facture', 'Facture'),
        ('proforma', 'Proforma'),
        ('avoir', 'Avoir'),
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
    invoice_number = models.CharField(max_length=10, unique=True)
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='invoices')
    invoice_object = models.TextField(max_length=200)
    amount_ht = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_payer')

    def __str__(self):
        return f"Facture {self.invoice_number} - {self.client.entity_name}"
    
    @property
    def amount_ttc(self):
        return self.amount_ht * (1 + self.vat_rate / 100)
    
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
    

class Payment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Paiement de {self.amount}€ pour la facture {self.invoice.invoice_number}"
    

class comment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Commentaire du {self.date.strftime('%d/%m/%Y')}"