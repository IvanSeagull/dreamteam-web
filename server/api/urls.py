# api/urls.py
from django.urls import path
from .views import signup, login_view, profile_data

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login_view, name='login_view'),
    path('profile-data/', profile_data, name='profile_data'),
]
