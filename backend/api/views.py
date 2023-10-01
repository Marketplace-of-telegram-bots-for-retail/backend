from functools import reduce
from operator import or_

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete, IsAuthor
from api.serializers import (
    CategorySerializer,
    ProductReadOnlySerializer,
    ProductSerializer,
    ReviewListSerializer,
    ReviewSerializer,
)
from core.paginations import Pagination
from products.models import Category, Product, Review, ShoppingCart

from .serializers import ShoppingCartCreateSerializer, ShoppingCartSerializer


class CartViewSet(ReadOnlyModelViewSet):
    '''Вьюсет для отображения корзины.'''
    queryset = ShoppingCart.objects.all()
    permission_classes = (IsAuthor, )
    serializer_class = ShoppingCartSerializer


class CategoryAPIView(ListRetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(CRUDAPIView):
    pagination_class = Pagination
    permission_classes = (AuthorCanEditAndDelete,)
    filter_backends = (
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ('^name',)
    ordering_fields = ('created', 'price')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProductReadOnlySerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action in ('list', 'retrieve'):
            categories = self.request.query_params.getlist('category')
            if categories:
                queryset = queryset.filter(
                    reduce(
                        or_,
                        [
                            Q(category__name=category)
                            for category in categories
                        ],
                    ),
                ).distinct()
            price = self.request.query_params.getlist('price')
            if price:
                queryset = queryset.filter(
                    Q(price__gte=int(price[0])) & Q(price__lte=int(price[1]))
                )
        return queryset

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthor])
    def shopping_cart(self, request, *args, **kwargs):
        '''Добавление товара в корзину.'''
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        cart_item, created = ShoppingCart.objects.get_or_create(
            user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = ShoppingCartCreateSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def remove_item(self, request, *args, **kwargs):
        '''Удаление товара из корзины.'''
        cart_item = ShoppingCart.objects.filter(
            user=request.user, product=kwargs.get('pk'))
        item_id = request.query_params.get('item_id')
        if not item_id and cart_item:
            cart_item.delete()
            return Response(
                'Весь товар удален полностью',
                status=status.HTTP_204_NO_CONTENT)
        if item_id and cart_item:
            cart_item = cart_item.filter(id=item_id)
            if cart_item:
                cart_item = cart_item.first()
                if cart_item.quantity == 1:
                    return Response(
                        'Должен быть хотя бы один объект данного типа',
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    cart_item.quantity -= 1
                    cart_item.save()
                return Response(
                    'Удален один товар', status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReviewListSerializer
        return ReviewSerializer

    @action(
        detail=True, methods=['POST'], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        model_obj = get_object_or_404(Review, user=user, product=product)
        model_obj.is_favorite = True
        model_obj.save()
        return Response(status=HTTP_200_OK)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        model_obj = get_object_or_404(Review, user=user, product=product)
        model_obj.is_favorite = False
        model_obj.save()
        return Response(status=HTTP_200_OK)

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        return product.reviews.all()

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(user=self.request.user, product=product)


class OrderViewSet(ModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def create(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def update(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})
