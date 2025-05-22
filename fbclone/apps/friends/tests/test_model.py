from django.test import TestCase
from friends.models import Friend, FriendRequest
from users.models import FbUser


class TestModels(TestCase):
    
    def setUp(self):
        self.user1 = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.user2 = FbUser.objects.create_user(username="user2", email="user2@example.com", password="12345678")
        self.frequest = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)

    def test_friend_request(self):
        self.assertEqual(self.frequest.sender, self.user1)
        self.assertEqual(self.frequest.receiver, self.user2)
        self.assertFalse(self.frequest.accepted)
        self.frequest.accept()
        self.assertTrue(self.frequest.accepted)
        self.assertEqual(self.frequest.__str__(), f"{self.user1} to {self.user2}")

    def test_not_friends(self):
        self.assertFalse(Friend.check_friend(self.user1, self.user2))
    
    def test_friends(self):
        self.frequest.accept()
        self.assertTrue(Friend.check_friend(self.user1, self.user2))
        
        