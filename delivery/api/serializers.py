from rest_framework import serializers
from delivery.models import Address, Driver, Service

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'latitude', 'longitude']
        
class DriverSerializer(serializers.ModelSerializer):
    location = AddressSerializer()
    
    class Meta:
        fields = ['id', 'name', 'location', 'is_available']
        
class ServiceSerializer(serializers.ModelSerializer):
    pickup_address = AddressSerializer()
    driver = DriverSerializer()
    
    class Meta:
        model = Service
        fields = ['id', 'pickup_address', 'driver', 'status', 'estimated_arrival_time', 'created_at']