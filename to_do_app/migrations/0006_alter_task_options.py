# Generated by Django 4.1 on 2023-01-19 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_app', '0005_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created']},
        ),
    ]
