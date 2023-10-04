from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    '''Сериализатор для модели User.'''

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'is_bayer',
            'is_seller',
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key != 'id':
                if key == 'email':
                    instance.email = value
                    instance.set_username()
                else:
                    setattr(instance, key, value)
        instance.save()
        return instance


class CustomUserCreateSerializer(UserCreateSerializer):
    '''Сериализатор для создания пользователя.'''

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
        )

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user


class CustomUserCreatePasswordRetypeSerializer(CustomUserCreateSerializer):
    '''Сериализатор для подтверждения пароля.'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['re_password'] = serializers.CharField(
            style={'input_type': 'password'},
        )

    default_error_messages = {
        'password_mismatch': (
            settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR,
        ),
    }

    def validate(self, attrs):
        self.fields.pop('re_password', None)
        re_password = attrs.pop('re_password')
        attrs['username'] = attrs['email']
        attrs = super().validate(attrs)
        if attrs['password'] == re_password:
            return attrs
        else:
            self.fail('password_mismatch')