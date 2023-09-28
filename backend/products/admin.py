from django.contrib import admin

from core.admin import BaseAdmin
from products.models import Category, Product


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
