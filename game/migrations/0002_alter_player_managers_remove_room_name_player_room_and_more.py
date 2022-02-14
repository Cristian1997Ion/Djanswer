# Generated by Django 4.0.2 on 2022-02-13 17:49

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='player',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
        migrations.AddField(
            model_name='player',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='game.room'),
        ),
        migrations.AddField(
            model_name='room',
            name='code',
            field=models.CharField(default='error', error_messages={'unique': 'This code was already taken. Please try again.'}, max_length=6, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*', 'Only alphanumerical characters.')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.RegexValidator('^.*[a-z]+.*$', 'At least one lowercase letter must be present.'), django.core.validators.RegexValidator('^.*[A-Z]+.*$', 'At least one uppercase letter must be present.'), django.core.validators.RegexValidator('^.*[0-9]+.*$', 'At least one digit must pe present.')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.'), django.core.validators.RegexValidator('^.*[a-zA-Z]+.*$', 'At least one letter must pe present.'), django.core.validators.RegexValidator('^[a-zA-Z]+.*$', 'The first character must be a letter.')]),
        ),
    ]