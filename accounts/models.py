from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(),
                                related_name='profile',
                                verbose_name='Профиль',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Аватар',
                               upload_to='avatars/',
                               null=True,
                               blank=True)
    git = models.URLField(max_length=200,
                          verbose_name='GIT',
                          null=True,
                          blank=True)
    about = models.TextField(max_length=2000,
                             verbose_name='О себе',
                             null=True,
                             blank=True
                             )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль: {self.user}. {self.id}'
