from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to return unread messages for a specific user.
    Usage: Message.unread.unread_for_user(user)
    """
    def unread_for_user(self, user):
        # Return messages where the user is the receiver and read=False
        return self.get_queryset().filter(receiver=user, read=False)
