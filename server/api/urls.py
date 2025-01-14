# api/urls.py
from django.urls import path
from .views import signup, login_view

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login_view, name='login_view'),
    # path('profile', profile, name='profile'),
    # Other routes...
]
