from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import CustomUserCreationForm

from django.http import JsonResponse

@csrf_protect
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created!")
            return redirect("login_view")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

@csrf_protect
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome {user.username}!")

                next_url = request.GET.get('next', 'http://localhost:8080/')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def profile_data(request):
    """
    GET /api/profile-data/
    Return user data as JSON if authenticated, or a 401 JSON error if not.
    """
    if not request.user.is_authenticated:
        print("Not logged in")
        return JsonResponse({'error': 'Not logged in'}, status=401)

    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'date_of_birth': user.date_of_birth,
    }
    return JsonResponse(data, status=200)


@csrf_exempt
def logout_view(request):
    print("WTF")
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out'}, status=200)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)