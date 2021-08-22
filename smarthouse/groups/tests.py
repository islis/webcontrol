from django.test import TestCase
from django.urls import reverse
from groups.models import Room
from django.contrib.auth.models import User


class RoomView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('Norm', 'norm@example.com', '123')
        self.superuser = User.objects.create_superuser('Admin', 'admin@example.com', '123')
        self.room = Room.objects.create(name='test room', owner=self.superuser)
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.user.delete()
        self.superuser.delete()
        self.room.delete()

    def test_create_room(self):
        create_url = reverse('room:add_room')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200, 'Create room is ok')

    def test_edit_room(self):
        self.client.force_login(self.superuser)
        edit_url = reverse('room:edit_room', args=(self.room.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200, 'User can edit this room')

    def test_edit_room_no_access(self):
        edit_url = reverse('room:edit_room', args=(self.room.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 403, 'User cant edit this room')

    def test_delete_room(self):
        self.client.force_login(self.superuser)
        edit_url = reverse('room:delete_room', args=(self.room.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200, 'User can delete this room')
