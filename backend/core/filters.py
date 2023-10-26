import django_filters
from django.db.models import Q

from products.models import Product


class NameOrDescriptionFilter(django_filters.FilterSet):
    """Кастомный фильтр для поиска по двум полям(name и description)"""

    search = django_filters.CharFilter(method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    class Meta:
        model = Product
        fields = ['search']
