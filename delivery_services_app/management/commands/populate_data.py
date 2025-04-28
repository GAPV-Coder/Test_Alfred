from django.core.management.base import BaseCommand
from faker import Faker
from delivery_services_app import Address, Driver

class Command(BaseCommand):
    help = 'Populating the database with false data'
    
    def handle(self, *args, **kwargs):
        fake = Faker('es_MX')
        for _ in range(30):
            Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                lalitude=fake.latitude(),
                longitude=fake.longitude()
            )
            
        addresses = Address.objects.all()
        for _ in range(25):
            Driver.objects.create(
                name=fake.name(),
                location=fake.random_element(addresses),
                is_available=True
            )
            
        self.stdout.write(self.style.SUCCESS('Fake data successfully generated.'))