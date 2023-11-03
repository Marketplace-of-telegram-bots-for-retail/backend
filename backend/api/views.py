from functools import reduce
from operator import or_

from django.db.models import F, Max, Min, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.mixins import CRUDAPIView, ListRetrieveAPIView, OrderAPIView
from api.permissions import AuthorCanEditAndDelete, IsOwner, IsOwnerOrder
from api.serializers import (
    CategorySerializer,
    FavoriteSerializer,
    OrderSerializer,
    ProductReadOnlySerializer,
    ProductSerializer,
    ReviewListSerializer,
    ReviewSerializer,
    ShoppingCartSerializer,
)
from backend.settings import PROMOCODE
from core.filters import NameOrDescriptionFilter
from core.paginations import Pagination
from products.models import (
    Category,
    Favorite,
    Order,
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
        ),
    ),
)
class CartViewSet(ReadOnlyModelViewSet):
    '''Корзина.'''

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return ShoppingCart.objects.filter(owner=self.request.user)

    @action(methods=['post'], detail=False, permission_classes=(IsOwner,))
    def promocode(self, request, *args, **kwargs):
        '''Ввод промокода для скидки.'''

        promocode = request.data.get('promocode')
        cart = get_object_or_404(ShoppingCart, owner=self.request.user)
        context = {'request': request, 'promocode': PROMOCODE.get(promocode)}
        serializer = ShoppingCartSerializer(cart, context=context)
        if promocode in PROMOCODE:
            cart.discount = PROMOCODE[promocode]
            cart.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                'Некорректный промокод',
                status=status.HTTP_400_BAD_REQUEST,
            )


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
        OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ('name', 'description')
    ordering_fields = ('created', 'price')
    filterset_class = NameOrDescriptionFilter

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

    @action(
        methods=['post', 'delete', 'patch'],
        detail=True,
        permission_classes=(IsOwner,),
    )
    def shopping_cart(self, request, *args, **kwargs):
        '''Добавление товара в корзину.'''

        product = get_object_or_404(Product, id=kwargs.get('pk'))
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            owner=request.user,
        )
        context = {'request': request}
        serializer = ShoppingCartSerializer(shopping_cart, context=context)
        if request.method == 'POST':
            cart_item, created = ShoppingCart_Items.objects.get_or_create(
                cart=shopping_cart,
                item=product,
            )
            if not created:
                cart_item.quantity = F('quantity') + 1
                cart_item.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )

        if request.method == 'DELETE':
            cart_item = get_object_or_404(
                ShoppingCart_Items,
                cart=shopping_cart,
                item=product,
            )
            cart_item.delete()
            if not ShoppingCart_Items.objects.filter(
                cart=shopping_cart,
            ).exists():
                ShoppingCart.objects.get(owner=request.user).delete()
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            cart_item = get_object_or_404(
                ShoppingCart_Items,
                cart=shopping_cart,
                item=product,
            )
            if cart_item.quantity > 1:
                cart_item.quantity = F('quantity') - 1
                cart_item.save()
            else:
                return Response(
                    f'Нельзя удалить товар {product} данным способом.',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, permission_classes=(IsOwner,))
    def select(self, request, *args, **kwargs):
        '''Выбор элемента в корзине.'''

        product = get_object_or_404(Product, id=kwargs.get('pk'))
        shopping_cart, _ = ShoppingCart.objects.get_or_create(
            owner=request.user,
        )
        context = {'request': request}
        serializer = ShoppingCartSerializer(shopping_cart, context=context)
        if request.method == 'PATCH':
            ShoppingCart_Items.objects.filter(
                item=product,
                cart=shopping_cart,
            ).update(is_selected=~F('is_selected'))
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['patch', 'delete'],
        detail=False,
        permission_classes=(IsOwner,),
    )
    def select_all(self, request, *args, **kwargs):
        '''Выбор всех элементов в корзине.'''

        shopping_cart, created = ShoppingCart.objects.get_or_create(
            owner=request.user,
        )
        context = {'request': request}
        serializer = ShoppingCartSerializer(shopping_cart, context=context)
        if request.method == 'PATCH':
            ShoppingCart_Items.objects.filter(cart=shopping_cart).update(
                is_selected=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            ShoppingCart_Items.objects.filter(cart=shopping_cart).update(
                is_selected=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, permission_classes=(IsOwner,))
    def delete_all_selected(self, request, *args, **kwargs):
        '''Удаление всех выбранных элементов в корзине.'''

        shopping_cart = ShoppingCart.objects.get(owner=request.user)
        context = {'request': request}
        serializer = ShoppingCartSerializer(shopping_cart, context=context)
        ShoppingCart_Items.objects.filter(
            cart=shopping_cart,
            is_selected=True,
        ).delete()
        if not ShoppingCart_Items.objects.filter(cart=shopping_cart).exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
        summary='Получить список заказов',
        description=('Возвращает список заказов текущего пользователя'),
        parameters=[
            OpenApiParameter(
                name='is_paid',
                description=(
                    'При is_paid=True выводит все оплаченные заказы. '
                    'При is_paid=False выводит все неоплаченные заказы.'
                ),
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary='Создать заказ.',
        description=('Создаёт заказ из текущей корзины пользователя'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного заказа',
        description=('Возаращает данные конкретного заказа'),
    ),
    destroy=extend_schema(
        summary='Удалить заказ',
        description=('Удаляет заказ.'),
    ),
)
class OrderViewSet(OrderAPIView):
    '''Заказы покупателя.'''

    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrder,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ('is_paid',)
    ordering_fields = 'created'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request):
        serializer = OrderSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk):
        '''Удалить неоплаченный заказ'''

        order = get_object_or_404(
            Order,
            user=request.user,
            is_paid=False,
            id=pk,
        )
        order.delete()
        return Response(
            {'message': 'Заказ успешно удален'},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['patch'])
    def is_paid(self, request, pk):
        order = self.get_object()
        order.is_paid = True
        order.save()
        serializer = OrderSerializer(
            order,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary='Получить минимальную и максимальную стоимость бота',
    description=(
        'Возвращает минимальную и максимальную стоимость бота. Если данных '
        'нет, то возвращает `null`.'
    ),
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={'example': {'price__min': 500, 'price__max': 1000}},
        ),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_min_max_cost(request):
    return Response(
        Product.objects.all().aggregate(Min('price'), Max('price')),
        status=status.HTTP_200_OK,
    )
