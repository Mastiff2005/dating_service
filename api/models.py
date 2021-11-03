from django.db import models

from users.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    liking = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Симпатия'
        verbose_name_plural = 'Симпатии'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'liking'],
                name='unique follow')
        ]
