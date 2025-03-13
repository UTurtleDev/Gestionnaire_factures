from django.db import models

# Create your models here.

class Client(models.Model):
    entity_name = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.entity_name