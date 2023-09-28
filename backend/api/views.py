from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ReviewSerializer, ReviewListSerializer
from products.models import Product, Review


class ReviewViewSet(viewsets.ModelViewSet):
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
        return Response(status=status.HTTP_200_OK)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        model_obj = get_object_or_404(Review, user=user, product=product)
        model_obj.is_favorite = False
        model_obj.save()
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        return product.reviews.all()

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(user=self.request.user, product=product)
