from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                verbose_name='Логин',
                                help_text='Введите логин'
                                )
    email = models.EmailField(max_length=254,
                              unique=True,
                              )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'password',
                       'first_name',
                       'last_name'
                       ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',), name='unique_follower'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='forbidden_self_follow'
            ),
        )
        ordering = ('author',)

    def __str__(self):
        return (f'Подписчик {self.user.username[:15]}'
                f' на автора {self.author.username[:15]}')
