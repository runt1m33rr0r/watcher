# Generated by Django 2.2 on 2019-05-05 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20190505_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='save_locataion',
            new_name='save_location',
        ),
    ]
