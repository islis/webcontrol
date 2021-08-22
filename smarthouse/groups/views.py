from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from .forms import RoomForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Room
from device.models import Device
from django.urls import reverse_lazy
import logging

log = logging.getLogger(__name__)


class AddRoom(LoginRequiredMixin, FormView):
    login_url = 'user:login'
    form_class = RoomForm
    template_name = 'room/room_form.html'
    room: Room

    def form_valid(self, form: RoomForm):
        room = form.save(commit=False)
        room.owner = self.request.user
        room.save()

        self.room = room
        log.info(f'Комната {self.room} добавлена')
        return super().form_valid(form)

    def get_success_url(self):
        return self.room.get_absolute_url()


class RoomView(UserPassesTestMixin, DetailView):
    login_url = 'user:login'
    model = Room
    template_name = 'room/room_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object'].devices = Device.objects.filter(owner=self.request.user, room=ctx['object'].id)
        return ctx

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().owner


class RoomUpdate(UserPassesTestMixin, UpdateView):
    login_url = 'user:login'
    model = Room
    form_class = RoomForm
    template_name = 'room/room_edit.html'
    room: Room

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().owner

    def form_valid(self, form: RoomForm):
        room = form.save(commit=False)
        room.owner = self.request.user
        room.save()

        self.room = room
        log.info(f'Комната {self.room} обновлена')
        return super().form_valid(form)

    def get_success_url(self):
        return self.room.get_absolute_url()


class RoomDelete(UserPassesTestMixin, DeleteView):
    login_url = 'user:login'
    model = Room
    template_name = 'room/room_delete.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().owner

    def get_success_url(self):
        log.info(f'Комната {self.get_object().name} удалена')
        return reverse_lazy('main')
