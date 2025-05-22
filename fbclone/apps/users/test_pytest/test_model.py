import django
django.setup()
import pytest 
from users.models import FbUser

def test_user_model():
    email = "test12@example.com"
    username = "test12"
    first_name = "test"
    last_name = "user"
    password = "123456789"

    user = FbUser.objects.create_user(email=email, username=username,first_name=first_name,last_name=last_name)

    assert user.email == email