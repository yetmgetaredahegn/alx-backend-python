from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

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
    """
    Before a Message is saved, if it already exists and content changed,
    save the old content to MessageHistory and mark edited=True.
    This function will use instance.edited_by if the view/serializer set it.
    """
    # If instance.pk is falsy -> it's a new message, not an update
    if not instance.pk:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # Strange race—treat as new
        return

    # Only log if content actually changed
    if old.content != instance.content:
        # Create a history entry with the OLD content and the user that was set on the instance.
        MessageHistory.objects.create(
            message=old,  # reference the message being updated (old/new share same pk)
            old_content=old.content,
            edited_by=getattr(instance, 'edited_by', None)
        )
        # Mark the message as edited so UI can show "(edited)"
        instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    After a User is deleted, remove all messages, histories, and notifications
    related to that user.
    """
    # Delete messages the user sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete any MessageHistory entries the user created
    MessageHistory.objects.filter(edited_by=instance).delete()


    Notification.objects.filter(user=instance).delete()

    print(f"Cleaned up data related to deleted user: {instance.username}")
