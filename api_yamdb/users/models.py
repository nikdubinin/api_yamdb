from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserRole, UserManager


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.CharField(
        verbose_name='Описание',
        max_length=255,
        blank=True
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
