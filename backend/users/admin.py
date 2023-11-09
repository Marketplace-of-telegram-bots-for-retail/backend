from django.contrib import admin

from core.admin import BaseAdmin
from users.models import Seller, User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'photo',
        'is_seller',
        'is_active',
        'created',
        'modified',
    )


@admin.register(Seller)
class SellerAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'inn',
        'store_name',
        'organization_name',
    )
