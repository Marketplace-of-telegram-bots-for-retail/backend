from django.contrib import admin

from core.admin import BaseAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_bayer',
        'is_seller',
        'is_active',
        'created',
        'modified',
    )
