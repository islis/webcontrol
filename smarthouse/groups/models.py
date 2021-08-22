from django.db import models
from django.conf import settings
from django.urls import reverse


class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название помещения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Владелец')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def get_absolute_url(self):
        return reverse('room:detail_room', args=[self.id])
