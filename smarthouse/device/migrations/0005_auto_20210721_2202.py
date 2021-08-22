# Generated by Django 3.2.5 on 2021-07-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_auto_20210716_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='extra_state',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Расширенное состояние'),
        ),
        migrations.AlterField(
            model_name='device',
            name='state',
            field=models.CharField(choices=[('ON', 'Включено'), ('OFF', 'Выключено')], default='OFF', max_length=32, verbose_name='Состояние'),
        ),
    ]