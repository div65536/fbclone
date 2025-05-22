from django.test import TestCase
from users.models import FbUser


class UserModelTest(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        first_name = "Test"
        last_name = "User"
        password = "123456789"

        user = FbUser.objects.create_user(username="test12", email=email,first_name=first_name,last_name=last_name,password=password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)  
        self.assertFalse(user.is_superuser)

class SuperUserTest(TestCase):

    def test_create_super_user(self):
        email = "test@example.com"
        password = "123456789"

        super_user = FbUser.objects.create_superuser(email=email, password=password)

        self.assertEqual(super_user.email, email)
        self.assertTrue(super_user.check_password(password))
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_admin)
        self.assertTrue(super_user.is_superuser)