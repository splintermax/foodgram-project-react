from rest_framework import serializers
from rest_framework.serializers import Serializer

from models import Follow


class IsFollowed(Serializer):
    is_Followed = serializers.SerializerMethodField()

    def get_is_followed(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            author=data, user=self.context.get('request').user
        ).exists()
