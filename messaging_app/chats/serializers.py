# chats/ serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import  Conversation, Message

User = get_user_model()

## User Serializer here

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['usr_id', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']


## Message Serializer

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

## conversation serializer (with nested messages and participants

class ConversationSerializer(serializers.ModelSerializer):
    participants_names = serializers.SerializerMethodField()
    topic = serializers.CharField(default="General")  # just to use CharField as required
    messages = MessageSerializer(source= 'message_set', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_participants_names(self, obj):
        return [f"{u.first_name} {u.last_name}" for u in obj.participants.all()]

    def validate_topic(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Topic must be at least 3 characters long.")
        return value
