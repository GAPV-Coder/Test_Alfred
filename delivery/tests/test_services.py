from django.test import TestCase
from delivery.models import Address, Driver, Service
from delivery.services.service_manager import ServiceManager
from django.utils import timezone
from datetime import timedelta

class ServiceTestCase(TestCase):
    def setUp(self):
        # Create addresses
        self.address1 = Address.objects.create(
            street='123 Main St',
            city='Mexico City',
            latitude=19.4326,
            longitude=-99.1332
        )
        self.address2 = Address.objects.create(
            street='TV56 La Paz St',
            city='Cartagena de Indias',
            latitude=10.3932,
            longitude=-75.4832
        )

        # Create an available driver
        self.driver = Driver.objects.create(
            name='Test Driver',
            location=self.address1,
            is_available=True
        )

    def test_find_nearest_driver(self):
        """
        Try the search for the nearest driver.
        """
        result = ServiceManager.find_nearest_driver(self.address2)
        self.assertIsNotNone(result)
        driver, distance, estimated_time = result
        self.assertEqual(driver, self.driver)
        self.assertGreater(distance, 0)
        self.assertGreater(estimated_time, 0)

    def test_create_service(self):
        """
        Test the creation of a service with an assigned driver.
        """
        service, error = ServiceManager.create_service(self.address2)
        self.assertIsNone(error)
        self.assertIsNotNone(service)
        self.assertEqual(service.pickup_address, self.address2)
        self.assertEqual(service.driver, self.driver)
        self.assertEqual(service.status, 'IN_PROGRESS')
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.is_available)

    def test_create_service_no_drivers(self):
        """
        Test the creation of a service without available drivers.
        """
        self.driver.is_available = False
        self.driver.save()
        service, error = ServiceManager.create_service(self.address2)
        self.assertIsNone(service)
        self.assertEqual(error, 'No drivers are available.')