from functools import reduce
from operator import or_

from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly, AllowAny,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete, IsOwner
from api.serializers import (
    CategorySerializer,
    FavoriteSerializer,
    ItemSerializer,
    ProductReadOnlySerializer,
    ProductSerializer,
    ReviewListSerializer,
    ReviewSerializer,
    ShoppingCartSerializer,
)
from core.paginations import Pagination
from products.models import (
    Category,
    Favorite,
    Product,
    Review,
    ShoppingCart,
    ShoppingCart_Items,
)


@extend_schema_view(
    list=extend_schema(
        summary='Получить все данные корзины',
        description=(
            'Возвращает корзину для текущего пользователя, где '
            '`total_cost` - общая стоимость всех продуктов, '
            '`total_amount` - общее кол-во товаров в корзине, '
            '`items` - боты, у которых поле `quantity` - кол-во каждого бота.'
        )
    )
)
class CartViewSet(ReadOnlyModelViewSet):
    '''Корзина.'''

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        return ShoppingCart.objects.filter(owner=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary='Получить список категорий',
        description=('Возвращает список категорий.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретной категории',
        description=('Возвращает данные конкретной категории.'),
    ),
)
class CategoryAPIView(ListRetrieveAPIView):
    '''Категории.'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


@extend_schema_view(
    list=extend_schema(
        summary='Получить список товаров',
        description=('Возвращает список товаров.'),
        parameters=[
            OpenApiParameter(
                name='category',
                description=(
                    'Фильтрация по категориям. Передаём `id` категории.'
                ),
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='search',
                description=(
                    'Поиск по начальному вхождению, регистр учитывается.'
                ),
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='price',
                description=(
                    'Для фильтрации по цене передаём именно два параметра '
                    '`price`. Число в первом параметре `price` '
                    'рассматривается как `от`, а во втором параметре - `до`.'
                ),
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='ordering',
                description=(
                    'Сортировка. `ordering=-created` - `Сначала новые`. При '
                    '`GET` запросе без этого параметра данные отсортированы '
                    '`Сначала новые`. `ordering=created` - `Сначала старые`.'
                    ' `ordering=price` - `Сначала дешевые`. `ordering=-price`'
                    ' - `Сначала дорогие`.'
                ),
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='is_favorited',
                description=(
                    'Если `is_favorited=True`, то выводятся все товары, '
                    'которые текущий пользователь добавил в избранное.'
                ),
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary='Создать товар',
        description=('Создать товар.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного товара',
        description=('Возвращает данные конкретного товара.'),
    ),
    update=extend_schema(
        summary='Обновить данные товара целиком',
        description=('Обновить данные товара целиком.'),
    ),
    partial_update=extend_schema(
        summary='Обновить данные товара частично',
        description=('Обновить данные товара частично.'),
    ),
    destroy=extend_schema(
        summary='Удалить товар',
        description=('Удалить товар.'),
    ),
)
class ProductAPIView(CRUDAPIView):
    '''Продукты.'''

    pagination_class = Pagination
    permission_classes = (AuthorCanEditAndDelete,)
    filter_backends = (
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ('^name',)
    ordering_fields = ('created', 'price')

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'product': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        model_obj = get_object_or_404(model, user=user, product=product)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        '''Добавить товар в избранное.'''

        return self.post_method_for_actions(
            request=request,
            pk=pk,
            serializers=FavoriteSerializer,
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        '''Удалить товар из избранного.'''

        return self.delete_method_for_actions(
            request=request,
            pk=pk,
            model=Favorite,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProductReadOnlySerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action in ('list', 'retrieve'):
            is_favorited = self.request.query_params.get('is_favorited')
            if is_favorited == 'True' and self.request.user.is_authenticated:
                queryset = queryset.filter(
                    product_favorite__user=self.request.user,
                )
            categories = self.request.query_params.getlist('category')
            if categories:
                try:
                    queryset = queryset.filter(
                        reduce(
                            or_,
                            [
                                Q(category__id=category)
                                for category in categories
                                if category.isdigit()
                            ],
                        ),
                    ).distinct()
                except TypeError as error:
                    print(error)
            price = self.request.query_params.getlist('price')
            if price:
                queryset = queryset.filter(
                    Q(price__gte=int(price[0])) & Q(price__lte=int(price[1])),
                )
        return queryset

    @action(methods=['post', 'delete', 'patch'], detail=True,
            permission_classes=(IsOwner, ))
    def shopping_cart(self, request, *args, **kwargs):
        '''Добавление и удаление товара из корзины.'''

        product = get_object_or_404(Product, id=kwargs.get('pk'))
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            owner=request.user)
        if request.method == 'POST':
            context = {'request': request}
            _ = ItemSerializer(context=context)
            cart_item, created = ShoppingCart_Items.objects.get_or_create(
                cart=shopping_cart, item=product)
            if not created:
                cart_item.quantity = F('quantity') + 1
                cart_item.save()
                return Response(
                    f'Вы успешно увеличили количество товара {product} на 1.',
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    f'Вы успешно добавили товар {product} в корзину.',
                    status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            cart_item = get_object_or_404(
                ShoppingCart_Items, cart=shopping_cart, item=product)
            cart_item.delete()
            if not ShoppingCart_Items.objects.filter(
                    cart=shopping_cart).exists():
                ShoppingCart.objects.get(owner=request.user).delete()
            return Response(
                f'Товар удален из корзины пользователя {self.request.user}',
                status=status.HTTP_204_NO_CONTENT)

        if request.method == 'PATCH':
            cart_item = get_object_or_404(
                ShoppingCart_Items, cart=shopping_cart, item=product)
            if cart_item.quantity > 1:
                cart_item.quantity = F('quantity') - 1
                cart_item.save()
            else:
                return Response(
                    f'Нельзя удалить товар {product} таким образом.',
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                f'Вы успешно уменьшили кол-во товара {product} на 1.')


@extend_schema_view(
    list=extend_schema(
        summary='Получить список отзывов',
        description=('Возвращает список отзывов.'),
    ),
    create=extend_schema(
        summary='Создать отзыв',
        description=('Создать отзыв.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного отзыва',
        description=('Возвращает данные конкретного отзыва.'),
    ),
    update=extend_schema(
        summary='Обновить данные отзыва целиком',
        description=('Обновить данные отзыва целиком.'),
    ),
    partial_update=extend_schema(
        summary='Обновить данные отзыва частично',
        description=('Обновить данные отзыва частично.'),
    ),
    destroy=extend_schema(
        summary='Удалить отзыв',
        description=('Удалить отзыв.'),
    ),
)
class ReviewViewSet(ModelViewSet):
    '''Отзывы.'''

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReviewListSerializer
        return ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        return Review.objects.filter(product=product)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(user=self.request.user, product=product)


@extend_schema_view(
    list=extend_schema(
        summary='Получить список заказов (в разработке)',
        description=('Не работает.'),
    ),
    create=extend_schema(
        summary='Создать заказ (в разработке)',
        description=('Не работает.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного заказа (в разработке)',
        description=('Не работает.'),
    ),
    update=extend_schema(
        summary='Обновить данные заказа целиком (в разработке)',
        description=('Не работает.'),
    ),
    partial_update=extend_schema(
        summary='Обновить данные заказа частично (в разработке)',
        description=('Не работает.'),
    ),
    destroy=extend_schema(
        summary='Удалить заказ (в разработке)',
        description=('Не работает.'),
    ),
)
class OrderViewSet(ModelViewSet):
    '''Заказы.'''

    def list(self, request, *args, **kwargs):
        '''Получить список заказов (в разработке).'''

        return Response({'message': 'в разработке'})

    def create(self, request, *args, **kwargs):
        '''Создать заказ (в разработке).'''

        return Response({'message': 'в разработке'})

    def retrieve(self, request, *args, **kwargs):
        '''Получить данные конкретного заказа (в разработке).'''

        return Response({'message': 'в разработке'})

    def update(self, request, *args, **kwargs):
        '''Обновить данные заказа целиком (в разработке).'''

        return Response({'message': 'в разработке'})

    def partial_update(self, request, *args, **kwargs):
        '''Обновить данные заказа частично (в разработке).'''

        return Response({'message': 'в разработке'})

    def destroy(self, request, *args, **kwargs):
        '''Удалить заказ (в разработке).'''

        return Response({'message': 'в разработке'})
