from django_filters.rest_framework import FilterSet

from chats.models import Message

class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = {
            'sent_at': ['gt','lt']
        }