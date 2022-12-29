from rest_framework import serializers
# from aiohttp_rest_framework import serializers

from room.models import Conversations


class ConversationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversations
        fields = "__all__"