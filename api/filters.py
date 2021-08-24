from django_filters import rest_framework as filters

from api.models import Title


class TitleFilter(filters.FilterSet):
    year = filters.NumberFilter()
    year_gt = filters.NumberFilter(field_name='year', lookup_expr='gt')
    year_lt = filters.NumberFilter(field_name='year', lookup_expr='lt')

    category = filters.CharFilter(field_name='category__slug', lookup_expr='icontains')
    genres = filters.CharFilter(field_name='genres__slug')

    class Meta:
        model = Title
        fields = ['title', 'year', 'category', 'genres']
