from django.contrib.auth.models import User
from django.db import models
from twilio.rest import Client


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


class Conversations(models.Model):
    room_id = models.CharField(null=False, max_length=100)
    message = models.TextField(null=False)
    sender = models.CharField(max_length=15)
    receiver = models.CharField(max_length=15)
    sent_at = models.DateTimeField(null=True)
    # is_sent = models.BooleanField(default=False)
