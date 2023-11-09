from django.contrib import admin

from core.admin import BaseAdmin
from products.models import (
    Category,
    Favorite,
    Image,
    ImageProduct,
    Order,
    OrderProductList,
    Product,
    Review,
    ShoppingCart,
    ShoppingCart_Items,
)
from products.utils import cut_string


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
        'short_name',
        'article',
        'price',
        'is_active',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified')
    search_fields = ('name',)

    def short_name(self, obj):
        return cut_string(obj.name)

    short_name.short_description = 'название'


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    inlines = (OrderProductListInline,)
    list_display = ('pk', 'user', 'pay_method', 'is_paid', 'is_active')


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('pk', 'user', 'product', 'rating', 'short_text')

    def short_text(self, obj):
        return cut_string(obj.text)

    short_text.short_description = 'текст отзыва'


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


@admin.register(Image)
class ImageAdmin(BaseAdmin):
    list_display = ('pk', 'image')


@admin.register(ImageProduct)
class ImageProductAdmin(BaseAdmin):
    list_display = ('pk', 'image', 'product')
