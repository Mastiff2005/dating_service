from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
