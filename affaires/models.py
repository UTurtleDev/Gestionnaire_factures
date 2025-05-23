from django.db import models
from factures.models import Invoice


# Create your models here.

class Affaire(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.SET_NULL, null=True, related_name='affaires')
    client_entity_name = models.CharField(max_length=100, blank=True, null=True)
    affaire_number = models.CharField(max_length=10, unique=True, db_index=True)
    affaire_description = models.TextField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Affaire"
        verbose_name_plural = "Affaires"

    def __str__(self):
        return f"{self.affaire_number} : {self.client_entity_name}"
    
    def formatted_budget(self):
        return f"{self.budget:,.2f} €".replace(",", " ").replace(".", ",")
    @property
    def total_facture_ht(self):
        # Calcule le montant total des factures HT associées à cette affaire
        # en utilisant la relation inverse depuis le modèle Invoice
        # et en filtrant par l'affaire actuelle
        return sum(facture.amount_ht for facture in self.invoices.all())
    
    def formatted_total_facture_ht(self):
        return f"{self.total_facture_ht:,.2f} €".replace(",", " ").replace(".", ",")
    
    @property
    def reste_a_facturer(self):
        # Calcule le montant restant à facturer pour cette affaire
        return self.budget - self.total_facture_ht
    
    def formatted_reste_a_facturer(self):
        return f"{self.reste_a_facturer:,.2f} €".replace(",", " ").replace(".", ",")
    
    def save(self, *args, **kwargs):
        # Sauvegarde le nom du client
        if self.client:
            self.client_entity_name = self.client.entity_name
        super().save(*args, **kwargs)