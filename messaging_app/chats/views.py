from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from chats.filters import MessageFilter
from chats.pagination import DefaultPagination
from chats.permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationReadSerializer, ConversationWriteSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["participants__email"]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ConversationReadSerializer
        return ConversationWriteSerializer

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)

        # enforce participant check manually
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body"]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()
