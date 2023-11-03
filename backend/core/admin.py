from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_per_page = 40
