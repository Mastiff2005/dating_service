from django.urls import path

from users.views import signup
from .views import (
    profile_follow,
)

urlpatterns = [
    path('clients/create/', signup, name='signup'),
    path('clients/<int:pk>/match/', profile_follow, name='follow'),
]
