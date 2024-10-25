from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class for energy usage hourly in kwh
class usage(models.Model):
    # time in hours
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    # energy usage in kwh
    solar_energy_usage = models.FloatField()
    grid_energy_usage = models.FloatField()
    efficiency = models.FloatField(default=0)
    
class solar(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # time in hours
    time = models.DateTimeField()
    # energy usage in kwh
    solar_energy = models.FloatField()

class tariff(models.Model):
    # time in hours
    time = models.DateTimeField()
    # energy price in kwh
    tariff_price = models.FloatField()
