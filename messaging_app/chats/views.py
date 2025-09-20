from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def list(self, request, *args, **kwargs):
        """
        Explicitly list all conversations.
        """
        conversations = Conversation.objects.all()
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Explicitly create a new conversation and add the requesting user as a participant.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user)
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Custom action to send a message in an existing conversation.
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

    def list(self, request, *args, **kwargs):
        """
        Explicitly list all messages.
        """
        messages = Message.objects.all()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Explicitly create a message. Sender is always the logged-in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
