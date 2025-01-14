# api/urls.py
from django.urls import path
from .views import signup, login_view, profile_data, logout_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login_view'),
    path('profile-data/', profile_data, name='profile_data'),
    path('logout/', logout_view, name='logout_view'),
]
