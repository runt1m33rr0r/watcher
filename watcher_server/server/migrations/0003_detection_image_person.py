# Generated by Django 2.2 on 2019-05-04 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20190504_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('images', models.ManyToManyField(to='server.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Camera')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.City')),
            ],
        ),
    ]