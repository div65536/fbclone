from django.test import TestCase
from django.core.exceptions import ValidationError
from users.validators import usernameoremailvalidator

class TestValidator(TestCase):
    def test_usernameoremailvalidator_invalid_email(self):
        with self.assertRaises(ValidationError):
            usernameoremailvalidator("123")