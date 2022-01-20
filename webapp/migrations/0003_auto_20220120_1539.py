from django.db import migrations


def transfer_types(apps, schema_editor):
    Task = apps.get_model('webapp.Task')
    for task in Task.objects.all():
        task.types.set([task.type])


def rollback_transfer(apps, schema_editor):
    Task = apps.get_model('webapp.Task')
    for task in Task.objects.all():
        task.type.set(task.types.all())


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_task_types'),
    ]

    operations = [
        migrations.RunPython(transfer_types, rollback_transfer)
    ]