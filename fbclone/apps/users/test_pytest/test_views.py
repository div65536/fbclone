import pytest 
from users.models import FbUser
from django.urls import reverse

@pytest.fixture
def user(db):
    return FbUser.objects.create_user(first_name="test",last_name="user",email="test2@example.com",username="test12",password="123456789")

def test_login(client,user):
    client.force_login(user)
    response = client.post(reverse('users:login'))

    assert response.context['user'].is_authenticated is True
    assert response.context['user'] == user
    assert response.context['user'].is_active is True