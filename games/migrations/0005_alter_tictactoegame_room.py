# Generated by Django 4.1.6 on 2023-02-04 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_tictactoegame_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tictactoegame',
            name='room',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]