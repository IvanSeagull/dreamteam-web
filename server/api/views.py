import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .forms import CustomUserCreationForm
from .models import CustomUser, FriendRequest, Friend
from django.db.models import Q


from django.http import JsonResponse

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