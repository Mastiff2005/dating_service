from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from utils.image_processing import add_watermark


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Добавляем водяной знак на фото пользователя
    username = serializer.validated_data['username']
    img = serializer.validated_data['user_image']
    result = add_watermark(img)
    result.save(f'media/users/avatars/{username}_image.jpg')
    serializer.validated_data['user_image'] = (
        f'users/avatars/{username}_image.jpg'
    )

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
