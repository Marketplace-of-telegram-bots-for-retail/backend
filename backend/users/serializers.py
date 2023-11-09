from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.fields import Base64ImageField
from users.models import Seller

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    '''Сериализатор для модели User.'''

    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'photo',
            'is_seller',
        )

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PUT':
            instance.photo = None
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

    # def create(self, validated_data):
    #     validated_data['username'] = validated_data['email']
    #     user = User.objects.create_user(**validated_data)
    #     return user
    def create(self, validated_data):
        email = validated_data.get('email')
        if not email:
            raise serializers.ValidationError('Email is required')
        username = email.split('@')[0]
        validated_data['username'] = username
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


class EmailSerializer(serializers.ModelSerializer):
    '''Сериализатор для проверки email.'''

    class Meta:
        model = User
        fields = ('email',)


class SellerSerializer(serializers.ModelSerializer):
    '''Сериализатор для получения статуса продавца.'''

    class Meta:
        model = Seller
        fields = ('id', 'user', 'inn')
        read_only_fields = ('user',)

    def validate(self, attrs):
        if Seller.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError(
                {'errors': 'Вы уже являетесь продавцом!'},
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.get(pk=self.context['request'].user.id)
        user.is_seller = True
        user.save()
        return super().create(validated_data)


class SellerUpdateSerializer(serializers.ModelSerializer):
    '''Сериализатор для обновления данных продавца.'''

    logo = Base64ImageField(required=False)

    class Meta:
        model = Seller
        fields = (
            'id',
            'user',
            'inn',
            'logo',
            'store_name',
            'organization_name',
            'organization_type',
            'bank_name',
            'ogrn',
            'kpp',
            'bik',
            'payment_account',
            'correspondent_account',
        )
        read_only_fields = ('user',)

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PUT':
            (
                instance.logo,
                instance.store_name,
                instance.organization_name,
                instance.organization_type,
                instance.bank_name,
                instance.ogrn,
                instance.kpp,
                instance.bik,
                instance.payment_account,
                instance.correspondent_account,
            ) = (None, None, None, None, None, None, None, None, None, None)
            # instance.logo = None
            # instance.store_name = None
            # instance.organization_name = None
            # instance.organization_type = None
            # instance.bank_name = None
            # instance.ogrn = None
            # instance.kpp = None
            # instance.bik = None
            # instance.payment_account = None
            # instance.correspondent_account = None
        return super().update(instance, validated_data)
