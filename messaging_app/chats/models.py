import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import  timezone

# Create your models here.

# Enum choices for user roles

class UserRole(models.TextChoices):
    GUEST  = 'guest', 'Guest'
    HOST= 'host', 'Host'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    phone_number= models.CharField(max_length=20, null=True, blank=True)
    role= models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)
    create_at  = models.DateTimeField(default=timezone.now)

    # Remove unused username field and make email the USERNAME_FILED

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} ({self.email})"


class Conversation(models.Model):
    conversation_id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
