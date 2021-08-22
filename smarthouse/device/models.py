from django.db import models
from uuid import uuid4
from django.conf import settings
from django.urls import reverse


# Create your models here.

# Управление из админки
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название типа устройства')
    image = models.ImageField(upload_to='device_type', verbose_name='Изображение устройства')
    url = models.CharField(max_length=255, verbose_name='Ссылка на код')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'


# Может управлять пользователь
class Device(models.Model):
    STATE_ON = 'ON'
    STATE_OFF = 'OFF'
    STATE_UNDEFINED = 'UNDEFINED'
    STATES = (
        (STATE_ON, 'Включено'),
        (STATE_OFF, 'Выключено'),
        # (STATE_UNDEFINED, 'Не определено'),
    )

    name = models.CharField(max_length=50, verbose_name='Название устройства')
    unique_id = models.CharField(max_length=38, unique=True, verbose_name='ID устройства')
    state = models.CharField(choices=STATES, default=STATE_OFF, max_length=32, verbose_name='Состояние')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Владелец')
    extra_state = models.JSONField(null=True, default=None, blank=True, verbose_name='Расширенное состояние')
    room = models.ForeignKey('groups.Room', on_delete=models.SET_NULL, null=True, verbose_name='Комната')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(uuid4())
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Девайс'
        verbose_name_plural = 'Девайсы'

    def get_absolute_url(self):
        return reverse('device-info', args=[self.id])


# Может управлять пользователь
class DeviceToType(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип устройства')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')

    class Meta:
        verbose_name = 'Девайсы по группам'
        verbose_name_plural = 'Девайсы по группам'

    def __str__(self):
        return str(self.device)
