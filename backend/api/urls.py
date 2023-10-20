from django.urls import include, path
from rest_framework import routers

from api.views import (
    CartViewSet,
    CategoryAPIView,
    OrderViewSet,
    SellerOrderViewSet,
    ProductAPIView,
    ReviewViewSet,
    get_min_max_cost,
)

router = routers.DefaultRouter()
router.register('categories', CategoryAPIView, basename='categories')
router.register('products', ProductAPIView, basename='products')
router.register(
    r'products/(?P<product_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='orders')
router.register('seller_orders', SellerOrderViewSet, basename='seller_orders')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('get_min_max_cost/', get_min_max_cost),
]
