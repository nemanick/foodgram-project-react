from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import ValidationError


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='subscriber')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscribe_unique'
            )
        ]

    def clean(self) -> None:
        if self.user == self.author:
            raise ValidationError('Нельзя оформить подписку на самого себя')
