# chats/ serializers.py
from MySQLdb.converters import conversions
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
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


## conversation serializer (with nested messages and participants


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(source= 'message_set', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']