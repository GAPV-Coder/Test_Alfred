from django.db import models

class Service(models.Model):
    """
    Model representing a delivery service.
    """
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending')
        ('IN_PROGRESS', 'In Progress')
        ('COMPLETED', 'Completed')
    )
    
    pickup_adress = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='services')
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, related_name='services')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    estimated_arrival_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        
    def __str__(self):
        return f"Service {self.id} - {self.status}"