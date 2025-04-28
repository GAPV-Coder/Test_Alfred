from rest_framework import serializers
from delivery.models import Address, Driver, Service

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'latitude', 'longitude']
        
class DriverSerializer(serializers.ModelSerializer):
    location = AddressSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source='location', write_only=True
    )
    class Meta:
        model = Driver
        fields = ['id', 'name', 'location', 'location_id', 'is_available']
        
class ServiceSerializer(serializers.ModelSerializer):
    pickup_address = AddressSerializer()
    driver = DriverSerializer()
    
    class Meta:
        model = Service
        fields = ['id', 'pickup_address', 'driver', 'status', 'estimated_arrival_time', 'created_at']