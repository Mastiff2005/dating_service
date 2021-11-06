from django_filters import rest_framework as filters

from users.models import User
from utils.utils import haversine


class CustomFilter(filters.FilterSet):
    '''
    Кастомный фильтр, фильтрует пользователей по полу,
    имени, фамилии и максимальному удалению в км (расстояние
    меньше или равно заданному)
    '''

    distance_max = filters.NumberFilter(
        method='distance_filter',
        field_name='distance_max',
        label="Расстояние, км"
    )

    def distance_filter(self, queryset, name, value):
        queryset = User.objects.all()
        filtered_list = []
        params = self.request.query_params
        if params.get('distance_max'):
            dist_param = float(params['distance_max'])
            request_user_long = self.request.user.longitude
            request_user_lat = self.request.user.latitude
            for user in queryset:
                user_long = user.longitude
                user_lat = user.latitude
                distance = float(haversine(
                    request_user_long, request_user_lat,
                    user_long, user_lat
                ))
                if distance <= dist_param:
                    filtered_list.append(user)
            queryset = User.objects.filter(username__in=filtered_list)
        return queryset

    class Meta:
        model = User
        fields = ['distance_max', 'gender', 'first_name', 'last_name']
