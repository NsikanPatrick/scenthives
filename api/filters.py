from django_filters.rest_framework import FilterSet
from shop.models import Perfume


class PerfumeFilter(FilterSet):
    class Meta:
        model = Perfume
        fields = {
            'category': ['exact'],
            'price': ['gt', 'lt'],      # Implementing a range
        }