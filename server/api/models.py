from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    

class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_friend_requests", on_delete=models.CASCADE, default=1)
    receiver = models.ForeignKey(CustomUser, related_name="received_friend_requests", on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


class Friend(models.Model):
    first_user = models.ForeignKey(CustomUser, related_name="friendships_initiated", on_delete=models.CASCADE, default=1)
    second_user = models.ForeignKey(CustomUser, related_name="friendships_received", on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('first_user', 'second_user')

    def __str__(self):
        return f"{self.first_user.username} <-> {self.second_user.username}"