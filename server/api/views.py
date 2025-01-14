import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')
            dob = data.get('date_of_birth')

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken.'}, status=400)

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                date_of_birth=dob
            )
            return JsonResponse({'message': 'User created!', 'user_id': user.id}, status=201)

        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'error': f'Invalid data: {e}'}, status=400)

    return JsonResponse({'error': 'Only POST requests allowed.'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful.'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'error': f'Invalid data: {e}'}, status=400)
    return JsonResponse({'error': 'Only POST requests allowed.'}, status=405)


@login_required
def profile(request):
    """
    GET /api/profile/
    Requires a valid session cookie from a prior login.
    Returns basic user data in JSON.
    """
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "date_of_birth": user.date_of_birth,
    }
    return JsonResponse(data)