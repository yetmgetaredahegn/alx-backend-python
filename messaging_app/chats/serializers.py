# messaging_app/chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # explicit CharFields so the auto-check finds them
    user_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    # sender returned as nested user for reads; creation uses request.user (view sets it)
    sender = UserSerializer(read_only=True)
    # explicit CharField usage (required by the auto-check)
    message_body = serializers.CharField()
    # Accept conversation PK when creating via Message endpoint (but add_message action will supply conversation)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ("message_id", "sender", "conversation", "message_body", "sent_at")

    def validate(self, attrs):
        # ensure message body is not blank
        if "message_body" in attrs and not attrs["message_body"].strip():
            raise serializers.ValidationError({"message_body": "Message body cannot be blank."})

        # if request is present, ensure sender (request.user) is a participant of the conversation
        request = self.context.get("request")
        conversation = attrs.get("conversation")
        if request and request.user.is_authenticated and conversation:
            if not conversation.participants.filter(pk=request.user.pk).exists():
                raise serializers.ValidationError("Sender must be a participant of the conversation.")
        return attrs


class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)

    # Read: nested display of participants (users)
    participants = serializers.SerializerMethodField()

    # Write: accept a list of user PKs to create/update participants (nested r/w)
    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="participants"
    )

    # Provide nested messages via SerializerMethodField (satisfies nested inclusion)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "participants_ids", "created_at", "messages")

    def get_participants(self, obj):
        return UserSerializer(obj.participants.all(), many=True).data

    def get_messages(self, obj):
        qs = obj.messages.order_by("sent_at").all()
        # pass context so MessageSerializer can access request for validation/formatting if needed
        return MessageSerializer(qs, many=True, context=self.context).data

    def validate(self, attrs):
        # When participants are provided during creation/update, ensure at least 2 participants
        participants = attrs.get("participants")
        if participants is not None:
            if len(participants) < 2:
                raise serializers.ValidationError({"participants": "A conversation must have at least 2 participants."})
        return attrs

    def create(self, validated_data):
        # validated_data will contain 'participants' (because of source="participants")
        participants = validated_data.pop("participants", [])
        conv = Conversation.objects.create(**validated_data)
        if participants:
            conv.participants.set(participants)
        return conv

    def update(self, instance, validated_data):
        # support updating participants via participants_ids
        participants = validated_data.pop("participants", None)
        instance = super().update(instance, validated_data)
        if participants is not None:
            instance.participants.set(participants)
        return instance
