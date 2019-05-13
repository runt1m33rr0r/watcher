# Generated by Django 2.2.1 on 2019-05-13 16:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_settingscreationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='downscale_level',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
