# Generated by Django 4.0.2 on 2022-02-14 10:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_player_managers_remove_room_name_player_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='players', to='game.room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='secret',
            field=models.CharField(blank=True, default='', max_length=4, validators=[django.core.validators.RegexValidator('^[0-9+]', 'Only digit characters.')]),
        ),
    ]