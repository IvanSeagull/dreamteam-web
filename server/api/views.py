import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import CustomUser, FriendRequest, Friend, Hobby
from django.http import JsonResponse
from typing import Any, Dict, List
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from datetime import date, timedelta

@csrf_protect
def signup(request):
    next_url = request.POST.get('next') or request.GET.get('next') or 'http://localhost:5173/profile'

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created!")
            newUser = authenticate(
                request,
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1")
            )
            if newUser is not None:
                auth_login(request, newUser)
            return redirect(next_url +"/"+ newUser.username)
        else:
            print("Signup form is invalid.")
            return render(request, "signup.html", {"form": form, "next": next_url})
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form, "next": next_url})

@csrf_protect
def login_view(request):
    next_url = request.GET.get('next', 'http://localhost:5173/profile')
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
                return redirect(next_url +"/"+ user.username)
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "next": next_url})


def profile_data(request):
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
        'hobbies': list(user.hobbies.values('id', 'name', 'description'))
    }
    return JsonResponse(data, status=200)


@csrf_exempt
def logout_view(request):
    print("WTF")
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out'}, status=200)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@require_GET
def get_user_by_username(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    authenticated_user = request.user

    if Friend.objects.filter(first_user=authenticated_user, second_user=user).exists() or \
       Friend.objects.filter(first_user=user, second_user=authenticated_user).exists():
        friend_status = 'friends'
    elif FriendRequest.objects.filter(sender=authenticated_user, receiver=user).exists():
        friend_status = 'request_sent'
    elif FriendRequest.objects.filter(sender=user, receiver=authenticated_user).exists():
        friend_status = 'request_received'
    else:
        friend_status = 'not_friends'
    friends_count = Friend.objects.filter(first_user=user).count() + Friend.objects.filter(second_user=user).count()
    
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'date_of_birth': user.date_of_birth,
        'hobbies': list(user.hobbies.values('id', 'name', 'description')),
        'friend_status': friend_status,
        'friends_count': friends_count
    }
    return JsonResponse(data, status=200)

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            receiver_id = data.get('receiver_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        if not receiver_id:
            return JsonResponse({'error': 'Receiver ID is required'}, status=400)

        sender = request.user
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if sender == receiver:
            return JsonResponse({'error': 'Cannot send a friend request to yourself'}, status=400)
        
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return JsonResponse({'error': 'Friend request already sent'}, status=400)

        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return JsonResponse({'message': 'Friend request sent'}, status=201)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)



@login_required
def get_friends(request):
    username = request.GET.get('username')

    try:
        user = CustomUser.objects.get(username=username) if username else request.user
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    friends = Friend.objects.filter(Q(first_user=user) | Q(second_user=user))
    
    friends_data = []
    for friend in friends:
        other_user = friend.second_user if friend.first_user == user else friend.first_user
        friends_data.append({
            'id': other_user.id,
            'name': other_user.name,
            'username': other_user.username,
        })
    
    return JsonResponse({'friends': friends_data}, status=200)

@login_required
def get_friend_requests(request):
    incoming_requests = FriendRequest.objects.filter(receiver=request.user)

    requests_data = [
        {
            'id': friend_request.id,
            'sender_id': friend_request.sender.id,
            'sender_name': friend_request.sender.name,
            'sender_username': friend_request.sender.username,
        }
        for friend_request in incoming_requests
    ]

    return JsonResponse({'requests': requests_data}, status=200)


@csrf_exempt
@login_required
def accept_friend_request(request, request_id):

    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Friend request not found'}, status=404)

    Friend.objects.create(
        first_user=friend_request.sender,
        second_user=friend_request.receiver
    )

    friend_request.delete()

    return JsonResponse({'message': 'Friend request accepted'}, status=200)

@csrf_exempt
@login_required
def reject_friend_request(request, request_id):

    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Friend request not found'}, status=404)

    friend_request.delete()

    return JsonResponse({'message': 'Friend request rejected'}, status=200)

@require_GET
def get_all_hobbies(request) -> JsonResponse:
    """Get all available hobbies."""
    hobbies = list(Hobby.objects.values('id', 'name', 'description'))
    return JsonResponse({'hobbies': hobbies}, safe=False)

@csrf_exempt
@login_required
@require_POST
def add_hobby(request) -> JsonResponse:
    """Add a new hobby to the system."""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return JsonResponse({'error': 'Hobby name is required'}, status=400)
            
        hobby, created = Hobby.objects.get_or_create(
            name=name.lower().strip(),
            defaults={'description': description}
        )
        
        return JsonResponse({
            'hobby': {
                'id': hobby.id,
                'name': hobby.name,
                'description': hobby.description
            },
            'created': created
        }, status=201 if created else 200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@login_required
@require_GET
def get_similar_users(request) -> JsonResponse:
    """Get users with similar hobbies, with pagination and age filtering."""
    page = int(request.GET.get('page', 1))
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    per_page = 10
    
    current_user = request.user
    current_user_hobbies = set(current_user.hobbies.values_list('id', flat=True))
    
    # Base queryset excluding the current user
    users_qs = CustomUser.objects.exclude(id=current_user.id)
    
    # Apply age filtering if provided
    if min_age is not None:
        try:
            min_age = int(min_age)
            users_qs = users_qs.filter(date_of_birth__isnull=False)\
                             .exclude(date_of_birth__gt=date.today() - timedelta(days=min_age*365))
        except ValueError:
            return JsonResponse({'error': 'Invalid min_age parameter'}, status=400)
            
    if max_age is not None:
        try:
            max_age = int(max_age)
            users_qs = users_qs.filter(date_of_birth__isnull=False)\
                             .exclude(date_of_birth__lt=date.today() - timedelta(days=(max_age+1)*365))
        except ValueError:
            return JsonResponse({'error': 'Invalid max_age parameter'}, status=400)

    # Calculate common hobbies for each user
    users_with_common = []
    for user in users_qs:
        user_hobbies = set(user.hobbies.values_list('id', flat=True))
        common_hobbies = current_user_hobbies.intersection(user_hobbies)
        if common_hobbies:  # Only include users with at least one common hobby
            common_hobby_details = list(Hobby.objects.filter(id__in=common_hobbies).values('name'))
            users_with_common.append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'age': user.age,
                'common_hobbies': common_hobby_details,
                'common_hobbies_count': len(common_hobbies)
            })

    # Sort by number of common hobbies (descending)
    users_with_common.sort(key=lambda x: x['common_hobbies_count'], reverse=True)
    
    # Implement pagination
    paginator = Paginator(users_with_common, per_page)
    try:
        page_data = paginator.page(page)
    except Exception:
        return JsonResponse({'error': 'Invalid page number'}, status=400)

    return JsonResponse({
        'users': list(page_data),
        'total_pages': paginator.num_pages,
        'current_page': page,
        'total_users': len(users_with_common)
    })

@csrf_exempt
@login_required
@require_POST
def update_user_hobbies(request) -> JsonResponse:
    """Update the current user's hobbies."""
    try:
        data = json.loads(request.body)
        hobby_ids = data.get('hobby_ids', [])
        
        # Validate hobby IDs
        hobbies = Hobby.objects.filter(id__in=hobby_ids)
        if len(hobbies) != len(hobby_ids):
            return JsonResponse({'error': 'One or more invalid hobby IDs'}, status=400)
            
        # Update user's hobbies
        request.user.hobbies.set(hobbies)
        
        return JsonResponse({
            'hobbies': list(request.user.hobbies.values('id', 'name', 'description'))
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    

@csrf_exempt
@login_required
def update_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not password1 or not password2:
            return JsonResponse({'error': 'Both passwords are required'}, status=400)

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        user = request.user
        user.set_password(password1)
        user.save()
        update_session_auth_hash(request, user)

        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'name': request.user.name,
            'email': request.user.email,
            'date_of_birth': request.user.date_of_birth,
        }
        return JsonResponse({'user': user_data}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)