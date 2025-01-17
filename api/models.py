from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "hobbies"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, related_name='users', blank=True)

    def __str__(self) -> str:
        return self.username
    
    @property
    def age(self) -> int:
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return 0

class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_friend_requests", on_delete=models.CASCADE, default=1)
    receiver = models.ForeignKey(CustomUser, related_name="received_friend_requests", on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self) -> str:
        return f"{self.sender.username} -> {self.receiver.username}"

class Friend(models.Model):
    first_user = models.ForeignKey(CustomUser, related_name="friendships_initiated", on_delete=models.CASCADE, default=1)
    second_user = models.ForeignKey(CustomUser, related_name="friendships_received", on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('first_user', 'second_user')

    def __str__(self) -> str:
        return f"{self.first_user.username} <-> {self.second_user.username}"