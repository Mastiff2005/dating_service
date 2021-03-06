from django.contrib import admin
from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'liking')
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
