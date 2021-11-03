from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from users.views import signup
from .views import (
    profile_follow,
    UserViewSet
)

router = DefaultRouter()

router.register('list', UserViewSet, basename='users_list')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/create/', signup, name='signup'),
    path('clients/<int:pk>/match/', profile_follow, name='follow'),
]
