from django.db import models

class Driver(models.Model):
    """
    Model representing a driver with it's locations and availability status.
    """
    
    name = models.CharField(max_length=100)
    location = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='drivers')
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
        
    def __str__(self):
        return self.name
    