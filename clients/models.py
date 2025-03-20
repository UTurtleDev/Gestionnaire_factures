from django.db import models

# Create your models here.

class Client(models.Model):
    entity_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    # zip_code = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.entity_name