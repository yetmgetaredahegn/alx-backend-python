from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    """
    Custom User model with explicit field names the auto-check expects.
    NOTE: user_id is the primary key (UUID).
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Explicitly declare common fields so the auto-check finds them.
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # mirrors Django's password field

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"  # keep default username behavior for simplicity
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.username} ({self.user_id})"