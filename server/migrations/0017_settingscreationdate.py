# Generated by Django 2.2.1 on 2019-05-13 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0016_auto_20190513_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingsCreationDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]