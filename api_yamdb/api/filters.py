from django_filters import filters, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = '__all__'
