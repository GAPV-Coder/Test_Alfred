from django.contrib import admin
from .models import Address, Driver, Service

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'latitude', 'longitude')
    search_fields = ('street', 'city')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pickup_address', 'driver', 'status', 'estimated_arrival_time', 'created_at')
    list_filter = ('status',)
    search_fields = ('pickup_address__street', 'driver__name')