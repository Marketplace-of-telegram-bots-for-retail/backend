from django.urls import include, path
from rest_framework import routers

from api.views import (
    CartViewSet,
    CategoryAPIView,
    MyProductAPIView,
    OrderViewSet,
    ProductAPIView,
    ReviewViewSet,
    get_min_max_cost,
)
from users.views import become_seller, email_verification

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('categories', CategoryAPIView, basename='categories')
router.register('my_products', MyProductAPIView, basename='my_products')
router.register('orders', OrderViewSet, basename='orders')
router.register('products', ProductAPIView, basename='products')
router.register(
    r'products/(?P<product_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)

urlpatterns = [
    path('', include(router.urls)),
    path('users/become_seller/', become_seller),
    path('users/email_verification/', email_verification),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('get_min_max_cost/', get_min_max_cost),
    path('oauth/', include('social_django.urls', namespace='social')),
]
