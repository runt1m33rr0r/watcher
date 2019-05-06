# Generated by Django 2.2 on 2019-05-06 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20190506_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Camera')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.City')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Image')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Person')),
            ],
        ),
    ]
