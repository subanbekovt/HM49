# Generated by Django 4.0.1 on 2022-01-30 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_task_description_alter_task_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.CharField(max_length=2000, verbose_name='Описание')),
            ],
        ),
    ]