from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from .models import Conversation, Message

# Create your views here.

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ## only show conversation where the user is a participants
        return self.queryset.filter(participants=self.request.user)


    def perform_create(self, serializer):
        ## Automatically add the authenticated user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)




## Message viewset

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return messages in conversations the user participates in
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        # Prevent users from sending to conversations they’re not part of
        if not conversation.participants.filter(id=self.request.user.id).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)
