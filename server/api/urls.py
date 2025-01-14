# api/urls.py
from django.urls import path
from .views import signup, api_login, profile

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', api_login, name='login'),
    path('profile', profile, name='profile'),
    # Other routes...
]
