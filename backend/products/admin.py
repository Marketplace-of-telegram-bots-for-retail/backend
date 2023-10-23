from django.contrib import admin

from core.admin import BaseAdmin
from products.models import (
    Category,
    Favorite,
    Order,
    OrderProductList,
    Product,
    Review,
    ShoppingCart,
    ShoppingCart_Items,
)


class OrderProductListInline(admin.TabularInline):
    model = OrderProductList
    extra = 1


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
    inlines = (OrderProductListInline, )
    list_display = ('pk', 'user', 'is_paid', 'is_active')


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'product', 'rating', 'text')


@admin.register(OrderProductList)
class OrderProductListAdmin(BaseAdmin):
    list_display = ('pk', 'order', 'product', 'quantity')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(BaseAdmin):
    list_display = ('pk', 'owner', 'discount')


@admin.register(ShoppingCart_Items)
class ShoppingCart_ItemsAdmin(BaseAdmin):
    list_display = ('item', 'cart', 'quantity', 'is_selected')


@admin.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'product')
