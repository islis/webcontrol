# Generated by Django 3.2.5 on 2021-07-22 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('device', '0005_auto_20210721_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.room', verbose_name='Комната'),
        ),
    ]
