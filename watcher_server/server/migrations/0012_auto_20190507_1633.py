# Generated by Django 2.2 on 2019-05-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_detection_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
