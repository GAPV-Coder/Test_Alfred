from typing import Optional, Tuple
from django.db.models import QuerySet
from delivery.models import Address, Driver, Service
from .distance_calculator import DistanceCalculator
from django.utils import timezone
from datetime import timedelta

class ServiceManager:
    """
    Class to manage the service assignment logic.
    """
    @staticmethod
    def find_nearest_driver(pickup_address: Address) -> Optional[Tuple[Driver, float, float]]:
        """
        Find the closest available driver to the pickup address.
        Returns a tuple with (driver, distance, estimated time) or None if there are no drivers.
        """
        available_drivers = Driver.objects.filter(is_available=True)
        if not available_drivers.exists():
            return None
        
        nearest_driver = None
        min_distance = float('inf')
        estimated_time = 0.0
        
        for driver in available_drivers:
            distance = DistanceCalculator.calculate_distance(
                pickup_address.latitude, pickup_address.longitude,
                driver.location.latitude, driver.location.longitude
            )
            if distance < min_distance:
                min_distance = distance
                estimated_time = DistanceCalculator.calculate_estimated_time(distance)
                nearest_driver = driver
        
        return nearest_driver, min_distance, estimated_time
    
    @staticmethod
    def create_service(pickup_address: Address) -> Tuple[Service, Optional[str]]:
        """
        Creates a new service and assigns the nearest driver.
        Returns the created service and an error message if no drivers are available.
        """
        result = ServiceManager.find_nearest_driver(pickup_address)
        if not result:
            return None, "No drivers are available."
        
        driver, distance, estimated_time = result
        estimated_arrival = timezone.now() + timedelta(minutes=estimated_time)
        service = Service.objects.create(
            pickup_address=pickup_address,
            driver=driver,
            estimated_arrival_time=estimated_arrival,
            status='IN_PROGRESS'
        )
        driver.is_available = False
        driver.save()
        return service, None