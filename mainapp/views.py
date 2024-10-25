from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views import View
from .models import usage, solar, tariff
from django.shortcuts import render
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World!")


@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not username or not password or not email:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already taken'}, status=400)

            user = User.objects.create(
                username=username,
                password=make_password(password),  
                email=email
            )
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_data(request):
    return Response({"message": "You are authenticated!"})
    

def get_energy_data(request, user_id=1):
    # Fetch data from the models
    usage_data = usage.objects.filter(user_id=user_id).order_by('time')
    solar_data = solar.objects.filter(user_id=user_id).order_by('time')
    tariff_data = tariff.objects.all().order_by('time')  # assuming tariff is not user-specific

    # Prepare the combined data
    energy_data = []
    
    for usage_entry in usage_data:
        solar_entry = solar_data.filter(time=usage_entry.time).first()
        tariff_entry = tariff_data.filter(time=usage_entry.time).first()

        # Calculate cost from grid usage and tariff
        grid_cost = usage_entry.grid_energy_usage * tariff_entry.tariff_price if tariff_entry else 0
        
        # Structure the data in the desired format
        energy_data.append({
            'efficiency': usage_entry.efficiency,
            'datetime': usage_entry.time.strftime('%Y-%m-%d %H:%M:%S'),
            'time': usage_entry.time.strftime('%H:%M'),
            'usage': usage_entry.grid_energy_usage + (solar_entry.solar_energy if solar_entry else 0),
            'cost': round(grid_cost, 2),
            'solar': solar_entry.solar_energy if solar_entry else 0
        })

    return JsonResponse(energy_data, safe=False)


def predict_energy_data(request, user_id=1):
    # Fetch data from the models
    usage_data = usage.objects.filter(user_id=user_id).order_by('time')
    solar_data = solar.objects.filter(user_id=user_id).order_by('time')
    tariff_data = tariff.objects.all().order_by('time')  # assuming tariff is not user-specific

    # Prepare the data for linear regression
    times = np.array([entry.time.timestamp() for entry in usage_data]).reshape(-1, 1)
    grid_usage = np.array([entry.grid_energy_usage for entry in usage_data])
    solar_usage = np.array([entry.solar_energy_usage for entry in usage_data])
    solar_production = np.array([entry.solar_energy for entry in solar_data])
    tariffs = np.array([entry.tariff_price for entry in tariff_data])

    # Train the linear regression model
    model_grid = LinearRegression().fit(times, grid_usage)
    model_solar_usage = LinearRegression().fit(times, solar_usage)
    model_solar_production = LinearRegression().fit(times, solar_production)
    model_tariff = LinearRegression().fit(times, tariffs)

    # Predict the next hour
    next_time = (datetime.now() + timedelta(hours=1)).timestamp()
    next_time_array = np.array([[next_time]])

    predicted_grid_usage = model_grid.predict(next_time_array)[0]
    predicted_solar_usage = model_solar_usage.predict(next_time_array)[0]
    predicted_solar_production = model_solar_production.predict(next_time_array)[0]
    predicted_tariff = model_tariff.predict(next_time_array)[0]

    # Calculate the predicted cost
    predicted_cost = predicted_grid_usage * predicted_tariff

    # Structure the data in the desired format
    prediction_data = {
        'datetime': datetime.fromtimestamp(next_time).strftime('%Y-%m-%d %H:%M:%S'),
        'predicted_usage': predicted_grid_usage + predicted_solar_usage,
        'predicted_cost': round(predicted_cost, 2),
        'predicted_solar': predicted_solar_production
    }

    return JsonResponse(prediction_data, safe=False)



