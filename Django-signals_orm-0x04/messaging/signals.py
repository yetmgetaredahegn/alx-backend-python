from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    When a Message is created, automatically create a Notification
    for the receiver user.
    """
    if created:  # Only when the message is newly created
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=f"New message from {instance.sender.username}"
        )
