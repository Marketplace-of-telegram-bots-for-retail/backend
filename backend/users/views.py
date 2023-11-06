from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet
from drf_spectacular.utils import (
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import AuthorCanEditAndDelete
from users.models import Seller, User
from users.serializers import (
    CustomUserSerializer,
    SellerSerializer,
    SellerUpdateSerializer,
)


class CustomUserViewSet(UserViewSet):
    '''Кастомный вьюсет для пользователя.'''

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)


@extend_schema(
    summary=('Проверка на наличие пользователя с предоставленным email'),
    description=(
        'Возвращает `True`, если адрес электронной почты занят '
        'другим пользователем и `False`, если адрес электронной '
        'почты не используется.'
    ),
    request={
        status.HTTP_200_OK: OpenApiRequest(
            request={'example': {'email': 'test@test.ru'}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiRequest(
            request={'example': {}},
        ),
    },
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={'example': {'email_is_used': False}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={'example': {'email': ['Обязательное поле.']}},
        ),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def email_verification(request):
    data = request.data
    if not data.get('email', False):
        return Response(
            {'email': ['Обязательное поле.']},
            status=status.HTTP_400_BAD_REQUEST,
        )
    email = data['email']
    if not isinstance(email, str):
        return Response(
            {'email': ['Not a valid string.']},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        {'email_is_used': User.objects.filter(email=email).exists()},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    methods=['POST'],
    summary=('Получить статус продавца'),
    description=(
        'Получить статус продавца для пользователя, который отправил запрос.'
    ),
    request={
        status.HTTP_201_CREATED: OpenApiRequest(
            request={'example': {'inn': 1111211114}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiRequest(
            request={'example': {}},
        ),
    },
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response={'example': {'id': 1, 'user': 2, 'inn': '1111211114'}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={'example': {'inn': ['Обязательное поле.']}},
        ),
    },
)
@extend_schema(
    methods=['PATCH'],
    summary=('Изменить данные продавца частично'),
    description=(
        'Изменить данные продавца для пользователя, который отправил запрос.'
    ),
    request={
        status.HTTP_200_OK: OpenApiRequest(
            request={'example': {'inn': 2225455212}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiRequest(
            request={'example': {}},
        ),
    },
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={'example': {'id': 1, 'user': 2, 'inn': '2225455212'}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={'example': {'inn': ['Обязательное поле.']}},
        ),
    },
)
@extend_schema(
    methods=['DELETE'],
    summary=('Удалить данные продавца'),
    description=(
        'Удалить данные продавца для пользователя, который отправил запрос.'
    ),
    responses={
        status.HTTP_204_NO_CONTENT: OpenApiResponse(),
    },
)
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes([AuthorCanEditAndDelete])
def become_seller(request):
    '''Получить статус продавца.'''

    if request.method == 'POST':
        serializer = SellerSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    try:
        seller = Seller.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return Response(
            {'errors': 'Вы не являетесь продавцом!'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if request.method == 'PATCH':
        serializer = SellerUpdateSerializer(
            seller,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = User.objects.get(pk=seller.user.id)
    user.is_seller = False
    user.save()
    seller.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
