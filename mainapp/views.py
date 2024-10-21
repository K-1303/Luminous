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
