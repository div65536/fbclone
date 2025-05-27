import pytest 
from users.models import FbUser

@pytest.fixture
def user_a(db):
    return FbUser.objects.create_user(username="test01",email="test01@gmail.com",first_name="test01",last_name="user",password="123456789")

def test_foo(db,user_a):
    assert user_a.username == "test01"
    assert user_a.check_password("123456789") is True
    assert user_a.first_name == "Test01"
    assert user_a.last_name == "User"
    assert user_a.email == "test01@gmail.com"

