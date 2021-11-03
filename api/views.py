from django.shortcuts import render

from users.models import User


def index(request):
    user_list = User.objects.all()
    context = {'users': user_list}
    return render(request, 'index.html', context)
