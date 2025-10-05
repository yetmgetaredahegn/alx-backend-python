from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # It's a new message, not an edit
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content changed
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True  # mark it as edited