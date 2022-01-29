from django_filters import rest_framework as filters

from math import degrees, radians
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
        params = self.request.query_params
        if params.get('distance_max'):
            dist_param = float(params['distance_max'])

            request_user_long = self.request.user.longitude
            request_user_lat = self.request.user.latitude
            request_user_lat_rad, request_user_long_rad = map(
                radians, [request_user_lat, request_user_long]
            )
            # Добавлены условия, если вычисляемая долгот меньше 180
            # и больше 180, широта - меньше 0 или больше 90
            latitude_max_rad = (
                request_user_lat_rad + dist_param / 6371
                if (request_user_lat_rad + dist_param / 6371) <= 90 else 90
            )
            latitude_min_rad = (
                request_user_lat_rad - dist_param / 6371
                if (request_user_lat_rad - dist_param / 6371) >= 0 else 0
            )
            longitude_max_rad = (
                request_user_long_rad + dist_param / 6371
                if (request_user_long_rad + dist_param / 6371) <= 180
                else (request_user_long_rad + dist_param / 6371) - 360
            )
            longitude_min_rad = (
                request_user_long_rad - dist_param / 6371
                if (request_user_long_rad - dist_param / 6371) >= -180
                else 360 - (request_user_long_rad - dist_param / 6371)
            )

            latitude_max, longitude_max, latitude_min, longitude_min = map(
                degrees, [latitude_max_rad, longitude_max_rad,
                          latitude_min_rad, longitude_min_rad]
            )
            queryset = User.objects.filter(
                latitude__lte=latitude_max).filter(
                    longitude__lte=longitude_max).filter(
                        latitude__gte=latitude_min).filter(
                            longitude__gte=longitude_min)
            filtered_list = []
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
