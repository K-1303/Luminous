import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from mainapp.models import usage, solar, tariff  # Replace 'yourapp' with your actual app name
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Generate random data points for usage, solar, and tariff models'

    def handle(self, *args, **kwargs):
        # Number of data points to generate
        num_entries = 100

        # Function to create random datetime within the past year
        def random_datetime():
            now = timezone.now()
            delta = timedelta(days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            return now - delta

        # Function to create random solar energy usage
        def random_solar_energy():
            return round(random.uniform(0.1, 5.0), 2)  # Solar energy usage between 0.1 and 5.0 kWh

        # Function to create random grid energy usage
        def random_grid_energy():
            return round(random.uniform(0.1, 10.0), 2)  # Grid energy usage between 0.1 and 10.0 kWh

        # Function to create random tariff price
        def random_tariff_price():
            return round(random.uniform(0.05, 0.5), 2)  # Tariff price between $0.05 and $0.50 per kWh

        # Select a user to associate data with
        user = User.objects.first()  # Replace with a specific user if needed

        # Generate random data for the usage model
        for _ in range(num_entries):
            usage_entry = usage.objects.create(
                user_id=user,
                time=random_datetime(),
                solar_energy_usage=random_solar_energy(),
                grid_energy_usage=random_grid_energy()
            )
            usage_entry.save()

        # Generate random data for the solar model
        for _ in range(num_entries):
            solar_entry = solar.objects.create(
                user_id=user,
                time=random_datetime(),
                solar_energy=random_solar_energy()
            )
            solar_entry.save()

        # Generate random data for the tariff model
        for _ in range(num_entries):
            tariff_entry = tariff.objects.create(
                time=random_datetime(),
                tariff_price=random_tariff_price()
            )
            tariff_entry.save()

        self.stdout.write(self.style.SUCCESS(f'{num_entries} random data points added to usage, solar, and tariff models.'))
