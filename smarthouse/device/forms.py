from django.forms import ModelForm
from .models import Device
from groups.models import Room


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'room']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(owner=user)
