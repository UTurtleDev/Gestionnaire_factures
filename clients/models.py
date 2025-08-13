from django.db import models

# Create your models here.

class Client(models.Model):
    entity_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['entity_name']


    def __str__(self):
        return self.entity_name
    
    @property
    def contact_principal(self):
        return self.contacts.filter(is_principal=True).first()
    
    @property
    def tous_les_contacts(self):
        return self.contacts.all()
    
    @property
    def total_affaire_client(self):
        return sum(affaire.budget for affaire in self.affaires.all())
    
    def formatted_total_affaire_client(self):
        return f"{self.total_affaire_client:,.2f} €".replace(",", " ").replace(".", ",")
    

class Contact(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='contacts')
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    fonction = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_principal = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        # ordering = ['-is_principal', 'nom']
        ordering = ['nom']

        # Contrainte : un seul contact principal par client
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'is_principal'],
                condition=models.Q(is_principal=True),
                name='unique_principal_contact_per_client'
            )
        ]


    def __str__(self):
        nom_complet = f"{self.nom} {self.prenom}".strip()
        if self.fonction:
            return f"{nom_complet}"
        return nom_complet
    

    def save(self, *args, **kwargs):
        # Si on marque ce contact comme principal, 
        # démarquer les autres contacts principaux du même client
        if self.is_principal:
            self.__class__.objects.filter(
                client=self.client, 
                is_principal=True
            ).exclude(pk=self.pk).update(is_principal=False)
        
        # Si c'est le premier contact du client, le marquer automatiquement comme principal
        if not self.__class__.objects.filter(client=self.client).exists():
            self.is_principal = True
            
        super().save(*args, **kwargs)