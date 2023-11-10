from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet
from drf_spectacular.utils import (
    OpenApiParameter,
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
    EmailSerializer,
    SellerCreateSerializer,
    SellerSerializer,
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
        'Возвращает: `пользователь с таким адрес электронной почты уже '
        'существует.`, если адрес электронной почты занят другим '
        'пользователем и `False`, если адрес электронной почты не '
        'используется.'
    ),
    parameters=[
        OpenApiParameter(
            name='email',
            description=('Проверяемый email.'),
            required=True,
            type=str,
        ),
    ],
    request=EmailSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={'example': {'email': False}},
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                'example': {
                    'email': [
                        (
                            'пользователь с таким адрес электронной почты '
                            'уже существует.'
                        ),
                    ],
                },
            },
        ),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def email_verification(request):
    email = request.query_params.get('email')
    if not email:
        return Response(
            {'error': 'Отсутствует обязательный параметр email!'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    EmailSerializer(
        data={'email': f'{email}'},
        context={'request': request},
    ).is_valid(raise_exception=True)
    return Response(
        {'email': False},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    methods=['GET'],
    summary=('Получить данные продавца'),
    description=(
        'Получить данные продавца для пользователя, который отправил запрос.'
    ),
    responses=SellerSerializer,
)
@extend_schema(
    methods=['POST'],
    summary=('Получить статус продавца'),
    description=(
        'Получить статус продавца для пользователя, который отправил запрос.'
    ),
    request=SellerCreateSerializer,
    responses=SellerCreateSerializer,
)
@extend_schema(
    methods=['PUT'],
    summary=('Изменить данные продавца целиком'),
    description=(
        'Изменить данные продавца целиком для пользователя, '
        'который отправил запрос.'
    ),
    request=SellerSerializer,
    responses=SellerSerializer,
)
@extend_schema(
    methods=['PATCH'],
    summary=('Изменить данные продавца частично'),
    description=(
        'Изменить данные продавца частично для пользователя, '
        'который отправил запрос.'
    ),
    request=SellerSerializer(partial=True),
    responses=SellerSerializer,
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
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AuthorCanEditAndDelete])
def become_seller(request):
    '''Получить статус продавца.'''

    if request.user.is_anonymous:
        return Response(
            {'detail': 'Учетные данные не были предоставлены.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if request.method == 'POST':
        serializer = SellerCreateSerializer(
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
    if request.method == 'GET':
        return Response(
            SellerSerializer(seller).data,
            status=status.HTTP_200_OK,
        )
    if request.method == 'DELETE':
        user = User.objects.get(pk=seller.user.id)
        user.is_seller = False
        user.save()
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        serializer = SellerSerializer(
            seller,
            data=request.data,
            context={'request': request},
        )
    else:
        serializer = SellerSerializer(
            seller,
            data=request.data,
            context={'request': request},
            partial=True,
        )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
