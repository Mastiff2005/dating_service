from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_image = models.ImageField(upload_to='users/avatars/',
                                   default='no-avatar.png')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота

    REQUIRED_FIELDS = [
        'email', 'first_name', 'last_name', 'gender',
    ]

    def __str__(self):
        return self.username
