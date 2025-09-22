# chats/filters.py
from django_filters import rest_framework as filters
from chats.models import Message

class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            "sent_at": ["gt", "lt"],  # messages after/before a datetime
            "sender": ["exact"],      # optional: filter by sender
        }
