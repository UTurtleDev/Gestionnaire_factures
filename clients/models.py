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
        # Récupère le contact principal de la première affaire (ou None)
        premiere_affaire = self.affaires.first()
        if premiere_affaire:
            return premiere_affaire.contacts.filter(is_principal=True).first()
        return None
    
    @property
    def tous_les_contacts(self):
        # Récupère tous les contacts de toutes les affaires du client
        from clients.models import Contact
        return Contact.objects.filter(affaire__client=self)
    
    @property
    def total_affaire_client(self):
        return sum(affaire.budget for affaire in self.affaires.all())
    
    def formatted_total_affaire_client(self):
        return f"{self.total_affaire_client:,.2f} €".replace(",", " ").replace(".", ",")
    

class Contact(models.Model):
    affaire = models.ForeignKey('affaires.Affaire', on_delete=models.SET_NULL, related_name='contacts', null=True)
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

        # Contrainte : un seul contact principal par affaire (si affaire existe)
        constraints = [
            models.UniqueConstraint(
                fields=['affaire', 'is_principal'],
                condition=models.Q(is_principal=True, affaire__isnull=False),
                name='unique_principal_contact_per_affaire'
            )
        ]


    def __str__(self):
        # Gérer les valeurs None
        nom = self.nom or ""
        prenom = self.prenom or ""
        nom_complet = f"{nom} {prenom}".strip()
        
        # Si pas de nom/prénom, utiliser l'email ou un placeholder
        if not nom_complet:
            if self.email:
                nom_complet = self.email
            else:
                nom_complet = "Contact sans nom"
        
        if self.fonction:
            return f"{nom_complet} - {self.fonction}"
        return nom_complet
    

    def save(self, *args, **kwargs):
        # Si on marque ce contact comme principal, 
        # démarquer les autres contacts principaux de la même affaire
        if self.is_principal and self.affaire:
            self.__class__.objects.filter(
                affaire=self.affaire, 
                is_principal=True
            ).exclude(pk=self.pk).update(is_principal=False)
        
        # Si c'est le premier contact de l'affaire, le marquer automatiquement comme principal
        if self.affaire and not self.__class__.objects.filter(affaire=self.affaire).exists():
            self.is_principal = True
            
        super().save(*args, **kwargs)