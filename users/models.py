from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = models.CharField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES,
        verbose_name='пол'
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name='широта'
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name='долгота'
    )
    user_image = models.ImageField(
        upload_to='users/avatars/', default='no-avatar.png',
        verbose_name='аватар'
    )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        img = Image.open(self.user_image.path)
        new_img = (300, 300)
        img.thumbnail(new_img)
        img.save(self.user_image.path)

    REQUIRED_FIELDS = [
        'email', 'first_name', 'last_name', 'gender',
    ]

    def __str__(self):
        return self.username
