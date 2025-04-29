from django.test import TestCase
from delivery.models import Address, Driver, Service
from django.utils import timezone
from datetime import timedelta

class ModelTestCase(TestCase):
    def setUp(self):
        # Create an address
        self.address = Address.objects.create(
            street='123 Main St',
            city='Mexico City',
            latitude=19.4326,
            longitude=-99.1332
        )

        # Create a driver
        self.driver = Driver.objects.create(
            name='Test Driver',
            location=self.address,
            is_available=True
        )

    def test_address_creation(self):
        """
        Test the creation of an address.
        """
        self.assertEqual(self.address.street, '123 Main St')
        self.assertEqual(self.address.city, 'Mexico City')
        self.assertEqual(self.address.latitude, 19.4326)
        self.assertEqual(self.address.longitude, -99.1332)
        self.assertEqual(str(self.address), '123 Main St, Mexico City')

    def test_driver_creation(self):
        """
        Test the creation of a driver.
        """
        self.assertEqual(self.driver.name, 'Test Driver')
        self.assertEqual(self.driver.location, self.address)
        self.assertTrue(self.driver.is_available)
        self.assertEqual(str(self.driver), 'Test Driver')

    def test_service_creation(self):
        """
        Test the creation of a service.
        """
        service = Service.objects.create(
            pickup_address=self.address,
            driver=self.driver,
            status='IN_PROGRESS',
            estimated_arrival_time=timezone.now() + timedelta(minutes=30)
        )
        self.assertEqual(service.pickup_address, self.address)
        self.assertEqual(service.driver, self.driver)
        self.assertEqual(service.status, 'IN_PROGRESS')
        self.assertEqual(str(service), f"Service {service.id} - IN_PROGRESS")