from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from rest_framework import serializers



User = get_user_model()


class RegisterSerializer(ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = ["user_id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)