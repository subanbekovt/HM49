# Generated by Django 4.0.1 on 2022-01-20 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20220120_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='type',
        ),
    ]