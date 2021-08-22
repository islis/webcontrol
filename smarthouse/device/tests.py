from django.test import TestCase
from django.urls import reverse
from device.models import Device
from groups.models import Room
from django.contrib.auth.models import User


class DeviceView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('Norm', 'norm@example.com', '123')
        self.superuser = User.objects.create_superuser('Admin', 'admin@example.com', '123')
        self.room = Room.objects.create(name='test room', owner=self.superuser)
        self.device = Device.objects.create(name='test device', owner=self.superuser)
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.user.delete()
        self.superuser.delete()
        self.room.delete()
        self.device.delete()

    def test_create_device_and_view(self):
        self.client.force_login(self.superuser)
        create_url = reverse('add_device')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200, 'Create device is ok')

        response = self.client.post(create_url, data={
            'name': 'creation-test',
            'room': self.room.id,
        })
        self.assertEqual(response.status_code, 302, response.content.decode())

        self.assertIn('/device/', response.headers['location'], 'location is ok')

        response = self.client.get(response.headers['location'])
        self.assertIn('creation-test', response.content.decode(), 'Check header in created')

    def test_create_device_without_rights(self):
        create_url = reverse('add_device')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200, 'Create device is ok')

        response = self.client.post(create_url, data={
            'name': 'creation-test',
            'room': self.room.id,
        })
        self.assertNotEqual(response.status_code, 302, response.content.decode())
        self.assertIn('Выберите корректный вариант.', response.content.decode(), 'Check without rights ok')

    def test_edit_device(self):
        self.client.force_login(self.superuser)
        edit_url = reverse('device-edit', args=(self.device.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200, 'User can edit this device')

    def test_edit_device_no_access(self):
        edit_url = reverse('device-edit', args=(self.device.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 403, 'User cant edit this device')

    def test_delete_device(self):
        self.client.force_login(self.superuser)
        edit_url = reverse('device-delete', args=(self.device.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200, 'User can delete this device')
