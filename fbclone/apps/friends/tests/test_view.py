from django.test import TestCase, Client
from users.models import FbUser
from django.urls import reverse
from friends.models import Friend, FriendRequest

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.user2 = FbUser.objects.create_user(username="user2", email="user2@example.com", password="12345678")
    
    def test_send_request(self):
        self.client.login(username="user1@example.com", password="12345678")
        self.client.post(reverse("friends:send_request"),{"receiver":self.user2.email})

        self.assertTrue(FriendRequest.objects.filter(sender=self.user1, receiver=self.user2).exists())
        self.assertFalse(Friend.check_friend(self.user1, self.user2))
    
    def test_get_requests_GET(self):
        self.client.login(username="user2@example.com", password="12345678")
        frequest = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)

        response = self.client.get(reverse("friends:get_requests"), follow=True)

        self.assertIn(frequest, response.context['requests'])
    
    def test_get_requests_POST(self):
        self.client.login(username="user1@example.com", password="12345678")
        frequest= FriendRequest.objects.create(sender=self.user2, receiver=self.user1)

        response = self.client.post(reverse("friends:get_requests"), {"sender":self.user2.email}, follow=True)

        self.assertTrue(Friend.check_friend(self.user1, self.user2))
    
    def test_get_friends(self):
        self.client.login(username="user1@example.com", password="12345678")
        frequest = FriendRequest.objects.create(sender=self.user2, receiver=self.user1)
        frequest.accept()
        friend_instance = Friend.objects.get(from_friend=self.user1)
        response = self.client.get(reverse("friends:get_friends"), follow=True)
        
        self.assertIn(friend_instance, response.context["friends"])