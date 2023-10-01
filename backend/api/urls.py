from django.urls import include, path
from rest_framework import routers

from api.views import (
    CartViewSet,
    CategoryAPIView,
    OrderViewSet,
    ProductAPIView,
    ReviewViewSet,
)

router = routers.DefaultRouter()
router.register('categories', CategoryAPIView, basename='categories')
router.register('products', ProductAPIView, basename='products')
router.register('orders', OrderViewSet, basename='orders')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
