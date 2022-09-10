from rest_framework import serializers

from chatroom.models import Message

class MessagesSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    room = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['name','room','text','timestamp']
