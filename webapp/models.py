from django.db import models
from django.core.validators import MinLengthValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Task(BaseModel):
    title = models.CharField(max_length=200,
                             null=False,
                             blank=False,
                             verbose_name="Краткое описание",
                             validators=(MinLengthValidator(5),))
    description = models.CharField(max_length=2000,
                                   null=True,
                                   blank=True,
                                   verbose_name="Полное описание",
                                   validators=(MinLengthValidator(10),))
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='statuses', verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', related_name='task_types', blank=True)
    project = models.ForeignKey('webapp.Project', on_delete=models.CASCADE, related_name='projects', verbose_name='Проект')

    def __str__(self):
        return f"{self.pk}. {self.title} - {self.status}"

    class Meta:
        db_table = 'Tasks'
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(BaseModel):
    status = models.CharField(max_length=200, null=False, blank=False, verbose_name="Статус")

    def __str__(self):
        return f"{self.status}"

    class Meta:
        db_table = 'Statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(BaseModel):
    type = models.CharField(max_length=200, null=False, blank=False, verbose_name="Тип")

    def __str__(self):
        return f"{self.type}"

    class Meta:
        db_table = 'Types'
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'


class Project(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата изменения")
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=2000, verbose_name="Описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = 'Projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

