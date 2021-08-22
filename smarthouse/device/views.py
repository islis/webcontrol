from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from smarthouse.mqtt_worker import mqtt_publish
import logging
from .forms import DeviceForm
from .models import Device

log = logging.getLogger(__name__)


class AddDevice(LoginRequiredMixin, FormView):
    login_url = 'user:login'
    form_class = DeviceForm
    template_name = 'device/device_form.html'
    device: Device

    def get_form(self, form_class=None):
        initial = {}
        if 'room' in self.request.GET:
            room_id = self.request.GET['room']
            initial = {'room': room_id}

        kwargs = self.get_form_kwargs()
        kwargs['initial'].update(initial)

        return self.form_class(
            user=self.request.user,
            **kwargs,
        )

    def form_valid(self, form):
        device = form.save(commit=False)
        device.owner = self.request.user
        device.save()
        log.info(f'Устройство {device.name} добавлено')
        self.device = device
        return super().form_valid(form)

    def form_invalid(self, form: DeviceForm):
        log.warning('Ошибка добавления устройства')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.device.get_absolute_url()


def device_state(request):
    device_id = request.POST.get('id')
    state = request.POST.get('state')
    if device_id is None or state is None:
        return HttpResponseBadRequest('Не найдены параметры: id и state')

    device = get_object_or_404(Device, unique_id=device_id, owner=request.user)
    device.state = state
    device.save(update_fields=['state'])
    log.info(f'Статут девайса {device_id} обновлён')
    mqtt_publish(device_id, device.state)  # Отправляем информацию на сервер MQTT
    return HttpResponse(f'Статут девайса {device_id} обновлён')


class DeviceView(LoginRequiredMixin, DetailView):
    login_url = 'user:login'
    model = Device
    template_name = 'device/device_detail.html'


class DeviceList(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Device
    template_name = 'device/device_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_list'] = Device.objects.filter(owner=self.request.user)
        return ctx


class DeviceDelete(UserPassesTestMixin, DeleteView):
    login_url = 'user:login'
    model = Device
    template_name = 'device/device_delete.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().owner

    def get_success_url(self):
        log.info(f'Устройство {self.get_object().name} удалено')
        return reverse('device-list')


class EditDevice(UserPassesTestMixin, UpdateView):
    login_url = 'user:login'
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_edit_form.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().owner

    def get_form(self, form_class=None):
        initial = {}
        if 'room' in self.request.GET:
            room_id = self.request.GET['room']
            initial = {'room': room_id}

        kwargs = self.get_form_kwargs()
        kwargs['initial'].update(initial)

        return self.form_class(
            user=self.request.user,
            **kwargs,
        )

    def form_valid(self, form):
        device = form.save(commit=False)
        device.owner = self.request.user
        device.save()
        log.info(f'Устройство {device.name} обновлено')
        return super().form_valid(form)

    def form_invalid(self, form: DeviceForm):
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
