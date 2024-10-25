from django.urls import path, include
from .views import secure_data, RegisterUser, get_energy_data, predict_energy_data, home



urlpatterns = [
    path('', home),
    path('secure-data/', secure_data),
    path('register/', RegisterUser.as_view(), name='register'),
    path('get_energy_data/', get_energy_data),
    path('predict_energy_data/', predict_energy_data)
]
