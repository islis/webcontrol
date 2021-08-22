from django.test import TestCase
from django.contrib.auth.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('bob', 'bob@mail.com', 's3cr3t')
        self.normal_user = User.objects.create_user('joe', 'joe@mail.com', 's3cr3t')

    def tearDown(self):
        self.superuser.delete()
        self.normal_user.delete()

    def test_createsuperuser(self):
        self.assertTrue(self.superuser.is_superuser, 'Test user.is_superuser')
        self.assertTrue(self.superuser.is_staff, 'Test user.is_staff')
        self.assertTrue(self.superuser.is_active, 'Test user.is_active')

    def test_normal_user(self):
        self.assertFalse(self.normal_user.is_superuser, 'Test not user.is_superuser')
        self.assertFalse(self.normal_user.is_staff, 'Test user.is_staff')
        self.assertTrue(self.normal_user.is_active, 'Test user.is_active')
