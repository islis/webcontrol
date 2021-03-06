# Generated by Django 3.2.5 on 2021-07-07 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название устройства')),
                ('unique_id', models.CharField(max_length=38, unique=True, verbose_name='ID устройства')),
                ('state', models.CharField(choices=[('ON', 'Включено'), ('OFF', 'Выключено')], max_length=32, verbose_name='Состояние')),
                ('extra_state', models.JSONField(verbose_name='Расширенное состояние')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название типа устройства')),
                ('image', models.ImageField(upload_to='device_type', verbose_name='Изображение девайса')),
                ('url', models.CharField(max_length=255, verbose_name='Ссылка на код')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceToType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.device')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.type')),
            ],
        ),
    ]
