import re

from django.contrib.auth import password_validation as pass_val

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                user=user,
                subscribe=subscribe
            ).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        label='Пароль',
        write_only=True
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!'
            )
        if not re.match(r'^[\w.@+-]+\Z', username, flags=re.ASCII):
            raise serializers.ValidationError(
                ('Имя пользователя может содержать латиницу, '
                 'цифры и знаки @ / . / + / - / _')
            )
        elif len(username) < 4:
            raise serializers.ValidationError(
                'Логин должен содержать не менее 3-х символов!'
            )
        return username

    def validate_first_name(self, first_name):
        if not first_name.istitle():
            raise serializers.ValidationError(
                'Имя должно начинаться с прописной буквы!'
            )
        elif len(first_name) < 2:
            raise serializers.ValidationError(
                'Имя должно содержать не менее 2-х символов!'
            )
        return first_name

    def validate_last_name(self, last_name):
        if not last_name.istitle():
            raise serializers.ValidationError(
                'Фамилия должна начинаться с прописной буквы!'
            )
        return last_name

    def validate_password(self, password):
        password_validators = pass_val.get_default_password_validators()
        errors = []
        for validator in password_validators:
            try:
                validator.validate(password)
            except serializers.ValidationError as error:
                errors.append(error)
        if errors:
            raise serializers.ValidationError(errors)
        return password

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')
        read_only_fields = ('__all__')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                user=user,
                subscribe=subscribe
            ).exists()
        return False

    def get_recipes_count(self, subscribe):
        return subscribe.recipes.count()


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'subscribe')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'subscribe')
            )
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = FollowingSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate(self, data):
        user = data.get('user')
        subscribe = data.get('subscribe')
        if user == subscribe:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя!'
            )
        return data
