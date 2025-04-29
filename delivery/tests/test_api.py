from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from delivery.models import Address, Driver, Service
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

class APITestCase(APITestCase):
    def setUp(self):
        # Set up client and user for authentication
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create an address for the driver
        self.driver_address = Address.objects.create(
            street='123 Main St',
            city='Mexico City',
            latitude=19.4326,
            longitude=-99.1332
        )

        # Create an available driver
        self.driver = Driver.objects.create(
            name='Test Driver',
            location=self.driver_address,
            is_available=True
        )

        # Create an address for the service
        self.service_address = Address.objects.create(
            street='TV56 La Paz St',
            city='Cartagena de Indias',
            latitude=10.3932,
            longitude=-75.4832
        )

        # Create a service in progress
        self.service = Service.objects.create(
            pickup_address=self.service_address,
            driver=self.driver,
            status='IN_PROGRESS',
            estimated_arrival_time=timezone.now() + timedelta(minutes=30)
        )

    def test_create_service_request(self):
        """
        Try creating a service with a new pick-up address.
        """
        url = reverse('service-request')
        data = {
            'pickup_address': {
                'street': '789 Pine St',
                'city': 'Monterrey',
                'latitude': 25.6866,
                'longitude': -100.3161
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'IN_PROGRESS')
        self.assertIsNotNone(response.data['driver'])
        self.assertEqual(response.data['pickup_address']['street'], '789 Pine St')
        
        # Verify that the driver is no longer available
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.is_available)

    def test_create_service_request_no_drivers(self):
        """
        Tests the creation of a service when no drivers are available.
        """
        # Mark the driver as unavailable
        self.driver.is_available = False
        self.driver.save()

        url = reverse('service-request')
        data = {
            'pickup_address': {
                'street': '789 Pine St',
                'city': 'Monterrey',
                'latitude': 25.6866,
                'longitude': -100.3161
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No drivers are available.')

    def test_complete_service(self):
        """
        Try marking a service as completed.
        """
        url = reverse('service-complete', kwargs={'pk': self.service.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')

        # Verify that the driver is available again
        self.driver.refresh_from_db()
        self.assertTrue(self.driver.is_available)

    def test_complete_service_not_found(self):
        """
        Try marking a non-existent service as completed.
        """
        url = reverse('service-complete', kwargs={'pk': 999})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Service with id 999 does not exist.')

    def test_complete_service_already_completed(self):
        """
        Try marking a completed service.
        """
        self.service.status = 'COMPLETED'
        self.service.save()

        url = reverse('service-complete', kwargs={'pk': self.service.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Service is already completed.')

    def test_unauthenticated_request(self):
        """
        Try accessing an endpoint without authentication.
        """
        self.client.credentials()  # Remover credenciales
        url = reverse('service-request')
        data = {
            'pickup_address': {
                'street': '789 Pine St',
                'city': 'Monterrey',
                'latitude': 25.6866,
                'longitude': -100.3161
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)