from django.contrib import admin
from .models import CustomUser, Friend, FriendRequest, Hobby


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(Hobby)

