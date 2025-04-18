from django.db import models
from factures.models import Invoice


# Create your models here.

class Affaire(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.SET_NULL, null=True, related_name='affaires')
    client_entity_name = models.CharField(max_length=100, blank=True, null=True)
    affaire_number = models.CharField(max_length=10, unique=True, db_index=True)
    affaire_description = models.TextField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    factures = models.ManyToManyField('factures.Invoice', related_name='affaires', blank=True, null=True)

    class Meta:
        verbose_name = "Affaire"
        verbose_name_plural = "Affaires"

    def __str__(self):
        return f"{self.affaire_number} : {self.client_entity_name}"
    
    def formatted_budget(self):
        return f"{self.budget:.2f} €".replace(",", " ").replace(".", ",")
    @property
    def total_facture_ht(self):
        # print("self.factures =", self.factures)
        # print("self.factures.all() =", self.factures.all())
        # print("invoice.amount_ht =", Invoice.amount_ht)
        return sum(facture.amount_ht for facture in self.factures.all()) 
    
    def save(self, *args, **kwargs):
        # Sauvegarde le nom du client
        if self.client:
            self.client_entity_name = self.client.entity_name
        super().save(*args, **kwargs)