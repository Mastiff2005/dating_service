from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import CustomFilter
from .models import Follow
from .viewsets import RetrieveListModelViewSet
from users.models import User
from users.serializers import UserSerializer
from utils.utils import custom_send_mail, haversine


def index(request):
    '''
    Функция для отрисовки главной страницы с помощью шаблона index.html,
    для тестирования функционала. Выводит список пользователей
    и информацию о них.
    '''
    user_list = User.objects.all()
    lon1, lat1 = request.user.longitude, request.user.latitude
    distances = {}
    for user in user_list:
        lon2, lat2 = user.longitude, user.latitude
        distance = haversine(lon1, lat1, lon2, lat2)
        distances[user] = distance
    context = {
        'users': user_list,
        'distances': distances
    }
    return render(request, 'index.html', context)


@api_view(['GET'])
def profile_follow(request, pk):
    follower = request.user
    following = get_object_or_404(User, pk=pk)
    follower_followers = [item.user for item in follower.following.all()]
    if following != follower:
        Follow.objects.get_or_create(user=follower, liking=following)
        if following in follower_followers:
            # oтправляем на почту уведомления
            custom_send_mail(following, follower)
            custom_send_mail(follower, following)
            return Response(
                {'email': following.email}, status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(RetrieveListModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter
    filterset_fields = ('gender', 'first_name', 'last_name')
