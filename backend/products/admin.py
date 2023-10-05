from django.contrib import admin

from core.admin import BaseAdmin
from products.models import (
    Category,
    Order,
    OrderProductList,
    Product,
    Review,
    ShoppingCart,
)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'is_active', 'created', 'modified')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'name',
        'description',
        'article',
        'price',
        'is_active',
        'created',
        'modified',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'is_paid', 'sale_status')


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'product', 'rating', 'text', 'is_favorite')


@admin.register(OrderProductList)
class OrderProductListAdmin(BaseAdmin):
    list_display = ('pk', 'order', 'product', 'quantity')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'product', 'quantity')