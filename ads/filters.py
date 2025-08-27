import django_filters
from .models import Ad

class AdFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Ad
        fields = ['category', 'is_active', 'status', 'price_min', 'price_max']
