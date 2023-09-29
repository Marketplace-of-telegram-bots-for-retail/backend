from django.urls import include, path
from rest_framework import routers

from api.views import CategoryAPIView, ProductAPIView, OrderViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryAPIView, basename='categories')
router.register('products', ProductAPIView, basename='products')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
