from django.db import models

class Service(models.Model):
    """
    Model representing a delivery service.
    """
    
    status = models.CharField(
        max_length=20,
        choices = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ],
        default='PENDING'
    )
    
    pickup_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='services')
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, related_name='services')
    estimated_arrival_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = "delivery"
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        
    def __str__(self):
        return f"Service {self.id} - {self.status}"