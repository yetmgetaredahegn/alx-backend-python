import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Custom User model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Conversation model
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.id}"


# Message model
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"
