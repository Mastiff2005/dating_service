from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'price')
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
