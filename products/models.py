from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='category')
    image_file = models.ImageField(
        upload_to='products/images/', default='no-image.png',
        verbose_name='Изображение'
    )
    image_url = models.URLField()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
