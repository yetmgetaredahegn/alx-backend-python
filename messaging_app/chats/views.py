from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def perform_create(self, serializer):
        """
        When creating a new conversation, add the requesting user as a participant.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Custom action to send a message in an existing conversation.
        Endpoint: POST /api/conversations/{id}/send_message/
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """
        Always set sender to logged-in user when creating a message.
        """
        serializer.save(sender=self.request.user)
