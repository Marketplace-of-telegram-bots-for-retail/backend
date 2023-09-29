from functools import reduce
from operator import or_

from django.db.models import Q
from rest_framework import filters

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete
from api.serializers import (
    CategorySerializer,
    ProductReadOnlySerializer,
    ProductSerializer,
)
from core.paginations import Pagination
from products.models import Category, Product


class CategoryAPIView(ListRetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(CRUDAPIView):
    pagination_class = Pagination
    permission_classes = (AuthorCanEditAndDelete,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
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
