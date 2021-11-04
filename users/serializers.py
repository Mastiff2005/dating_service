from rest_framework import serializers

from .models import User
from utils.utils import haversine


class UserSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(allow_empty_file=False, use_url=True)
    distance = serializers.SerializerMethodField('get_distance')

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'gender',
            'user_image',
            'distance',
        )

    def validate(self, data):
        required_fields = map(
            data.get, ['email', 'first_name', 'last_name']
        )
        if not all(item for item in required_fields):
            raise serializers.ValidationError(
                'Это поле не может быть пустым'
            )
        return data

    def get_distance(self, obj):
        user = self.context['request'].user
        lon1, lat1 = user.longitude, user.latitude
        lon2, lat2 = obj.longitude, obj.latitude
        distance = haversine(lon1, lat1, lon2, lat2)
        return distance
