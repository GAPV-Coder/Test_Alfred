from django.db import models

class Address(models.Model):
    """
    Model representing an address with geographic coordinates.
    """
    
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        app_label = "delivery"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        
    def __str__(self):
        return f"{self.street}, {self.city}"
    