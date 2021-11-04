from django_filters import rest_framework as filters

from users.models import User


class CustomFilter(filters.FilterSet):

    distance = filters.RangeFilter(
        method='distance_filter',
        field_name='distance'
    )

    def distance_filter(self, queryset, name, value):
        if value:
            return queryset.filter()
        return queryset

    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'distance']
