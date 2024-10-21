from django.urls import path
from .views import secure_data, RegisterUser



urlpatterns = [
    path('secure-data/', secure_data),
    path('register/', RegisterUser.as_view(), name='register'),

]
