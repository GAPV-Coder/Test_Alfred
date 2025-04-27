from django.db import models

class Address(models.model):
    """
    Model representing an address with geographic coordinates.
    """
    
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    logitude = models.FloatField()
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        
    def __str__(self):
        return f"{self.name}, {self.city}"
    