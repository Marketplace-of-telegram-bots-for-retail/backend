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
router.register(
    r'products/(?P<product_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register('orders', OrderViewSet, basename='orders')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include("djoser.urls.authtoken")),
]
