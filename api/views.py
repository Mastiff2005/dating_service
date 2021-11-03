from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Follow
from .viewsets import RetrieveListModelViewSet
from users.models import User
from users.serializers import UserSerializer


def index(request):
    user_list = User.objects.all()
    context = {
        'users': user_list
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
            send_mail(
                'Вы кому-то понравились!',
                f'Вы понравились {following.username}! '
                f'Почта участника: {following.email}',
                'info@dating-service.example',
                [follower.email],
                fail_silently=False,
            )
            send_mail(
                'Вы кому-то понравились!',
                f'Вы понравились {follower.username}! '
                f'Почта участника: {follower.email}',
                'info@dating-service.example',
                [following.email],
                fail_silently=False,
            )
            return Response(
                {'email': following.email}, status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(RetrieveListModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('gender', 'first_name', 'last_name')
