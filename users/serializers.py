from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(allow_empty_file=False, use_url=True)

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
