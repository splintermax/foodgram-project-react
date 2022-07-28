from django.shortcuts import get_object_or_404

from djoser.serializers import SetPasswordSerializer
from rest_framework import permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from models import Follow, User
from permissions import IsAuthOrCreateList
from serializers import (FollowSerializer, FollowingSerializer,
                               UserCreateSerializer, UserSerializer)
from mixins import IsFollowed


class UserViewSet(IsFollowed):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthOrCreateList,)

    serializer_classes = {
        'create': UserCreateSerializer,
        'me': UserSerializer,
        'set_password': SetPasswordSerializer,
        'subscriptions': FollowSerializer
    }

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return self.serializer_class

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password')
        )
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request, *args, **kwargs):
        followers = User.objects.filter(user=request.user)
        serializer = self.get_serializer(followers, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class SubscriptionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        follower = get_object_or_404(User, id=user_id)
        user = self.request.user
        data = {'subscribe': follower.id, 'user': user.id}
        serializer = FollowingSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        follower = get_object_or_404(User, id=user_id)
        user = self.request.user
        subscription = get_object_or_404(
            Follow, user=user, subscribe=follower
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
