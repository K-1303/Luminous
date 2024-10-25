import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from mainapp.models import usage, solar, tariff  
from django.contrib.auth.models import User

# Provided base data
base_data = [
    { 'time': '00:00', 'usage': 2, 'cost': 0.24, 'solar': 0 },
    { 'time': '03:00', 'usage': 1.5, 'cost': 0.15, 'solar': 0 },
    { 'time': '06:00', 'usage': 3, 'cost': 0.45, 'solar': 0.5 },
    { 'time': '09:00', 'usage': 5, 'cost': 0.75, 'solar': 2 },
    { 'time': '12:00', 'usage': 4, 'cost': 0.60, 'solar': 3 },
    { 'time': '15:00', 'usage': 4.5, 'cost': 0.68, 'solar': 2.5 },
    { 'time': '18:00', 'usage': 6, 'cost': 1.20, 'solar': 1 },
    { 'time': '21:00', 'usage': 3.5, 'cost': 0.53, 'solar': 0 },
]

class Command(BaseCommand):
    help = 'Generate random data points for usage, solar, and tariff models'

    def handle(self, *args, **kwargs):
        # Number of days to generate data for
        num_days = 60  # For example, generate data for 30 days

        # Variance for random fluctuation
        usage_variance = 0.25  # Adjust this to vary the usage randomly
        solar_variance = 0.4  # Variance for solar energy values
        cost_variance = 0.05  # Variance for cost values

        # Function to create a datetime for a specific day and time
        def specific_datetime(day_shift, time_str):
            base_time = datetime.strptime(time_str, '%H:%M').time()
            now = timezone.now()
            date_shift = now - timedelta(days=day_shift)
            return timezone.make_aware(datetime.combine(date_shift, base_time))

        # Function to add variance to a value
        def add_variance(value, variance):
            return max(round(value + random.uniform(-variance, variance), 2), 0)

        # Select a user to associate data with
        user = User.objects.first()  # Replace with a specific user if needed

        # Lists to hold the objects to be created
        usage_entries = []
        solar_entries = []
        tariff_entries = []

        # Generate data for multiple days
        for day_shift in range(num_days):
            for entry in base_data:
                # Generate the time for the current day
                entry_time = specific_datetime(day_shift - 30, entry['time'])

                # Add variance to the grid usage and solar production values
                grid_usage = add_variance(entry['usage'], usage_variance)
                solar_production = add_variance(entry['solar'], solar_variance)
                cost_value = add_variance(entry['cost'], cost_variance)

                # Solar energy usage should be <= solar energy produced
                if solar_production > 0:
                    solar_usage = min(add_variance(solar_production, solar_variance), grid_usage)
                else:
                    solar_usage = 0

                total_energy_cost = grid_usage * cost_value + solar_production * cost_value

                # Calculate efficiency
                if total_energy_cost > 0:
                    efficiency = round((solar_usage / total_energy_cost) , 2)
                else:
                    efficiency = 0

                # Create the usage data (grid and solar energy usage)
                usage_entry = usage(
                    user_id=user,
                    time=entry_time,
                    solar_energy_usage=solar_usage,
                    grid_energy_usage=grid_usage - solar_usage,  # Remaining usage from grid
                    efficiency=efficiency  # Assign calculated efficiency
                )
                usage_entries.append(usage_entry)
        
                # Create the solar data (solar energy produced)
                solar_entries.append(solar(
                    user_id=user,
                    time=entry_time,
                    solar_energy=solar_production
                ))
        
                # Create the tariff data (tariff based on usage cost)
                tariff_entries.append(tariff(
                    time=entry_time,
                    tariff_price=cost_value  # Using cost as a base for tariff price
                ))

        # Bulk create all entries
        usage.objects.bulk_create(usage_entries)
        solar.objects.bulk_create(solar_entries)
        tariff.objects.bulk_create(tariff_entries)

        self.stdout.write(self.style.SUCCESS(f'Generated data for {num_days} days with variance.'))