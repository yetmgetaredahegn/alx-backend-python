from django.db import models

# Create your models here.
from django.db import models

from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # read/unread tracking (Task 4)
    read = models.BooleanField(default=False)

    # edit tracking (from earlier tasks)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='edited_messages'
    )

    # threaded replies (Task 3)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    # Managers: keep default, add custom unread manager
    objects = models.Manager()
    unread = UnreadMessagesManager()  

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content[:40]}'


class MessageHistory(models.Model):
    """
    Stores previous versions of a Message before an edit overwrote them.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    # Which user performed the edit (nullable because signal may not always have it)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='message_histories'
    )

    def __str__(self):
        return f'History for message {self.message_id} at {self.edited_at}'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.text}"
