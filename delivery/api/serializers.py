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
    pickup_address = AddressSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    pickup_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source='pickup_address', write_only=True, required=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(), source='driver', write_only=True, required=True
    )
    
    class Meta:
        model = Service
        fields = ['id', 'pickup_address', 'pickup_address_id', 'driver', 'driver_id', 
                'status', 'estimated_arrival_time', 'created_at']
        extra_kwargs = {
            'pickup_address': {'read_only': True},
            'driver': {'read_only': True}
        }