from django.contrib import admin
from .models import Device, Type, DeviceToType

admin.site.register(Device)
admin.site.register(Type)
admin.site.register(DeviceToType)
# Register your models here.
