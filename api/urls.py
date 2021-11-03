from django.urls import path

from users.views import signup

urlpatterns = [
    path('clients/create/', signup, name='signup'),
]
