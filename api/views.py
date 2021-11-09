from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import CustomFilter
from .models import Follow
from .viewsets import RetrieveListModelViewSet
from products.models import Product
from products.serializers import ProductSerializer
from products import tasks
from users.models import User
from users.serializers import UserSerializer
from utils.utils import custom_send_mail, haversine


def index(request):
    '''
    Функция для запуска парсера товаров и отрисовки главной страницы
    с помощью шаблона index.html для тестирования функционала.
    Выводит список пользователей и информацию о них
    '''
    # Запуск парсера
    tasks.parse_products.delay()

    # Вывод списка пользователей
    user_list = User.objects.all()
    if not request.user.is_authenticated:
        lon1, lat1 = 0, 0
    else:
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
    '''
    Добавляет пользователя в список понравившихся. Если текущий
    пользователь находится в списке понравившихся добавляемого
    пользователя, в теле ответа возвращается email добавленного
    пользователя, на почты текущего и добавленного пользователей
    высылаются уведомления "Вы понравились..."
    '''
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
    '''
    Выводит список пользователей. Доступный метод - GET
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter


class ProductViewSet(viewsets.ModelViewSet):
    '''
    Выводит список товаров
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'price', 'category')
