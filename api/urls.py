# api/urls.py
from django.urls import path
from .views import (
    signup, login_view, profile_data, logout_view, 
    get_user_by_username, send_friend_request, 
    get_friends, get_friend_requests, 
    accept_friend_request, reject_friend_request,
    get_all_hobbies, add_hobby, get_similar_users,
    update_user_hobbies, update_password, update_general_info
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login_view'),
    path('profile-data/', profile_data, name='profile_data'),
    path('logout/', logout_view, name='logout_view'),
    path('similar/', get_similar_users, name='get_similar_users'),  
    path('users/<str:username>/', get_user_by_username, name='get_user_by_username'),
    path('friend-request/send/', send_friend_request, name='send_friend_request'),
    path('friends/', get_friends, name='get_friends'),
    path('friend-requests/', get_friend_requests, name='get_friend_requests'),
    path('friend-requests/<int:request_id>/accept/', accept_friend_request, name='accept_friend_request'),
    path('friend-requests/<int:request_id>/reject/', reject_friend_request, name='reject_friend_request'),
    path('hobbies/', get_all_hobbies, name='get_all_hobbies'),
    path('hobbies/add/', add_hobby, name='add_hobby'),
    path('hobbies/update/', update_user_hobbies, name='update_user_hobbies'),
    path('settings/general/', update_general_info, name='general_settings'),
    path('settings/password/', update_password, name='password_settings'),
]