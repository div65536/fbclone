from django.test import TestCase, Client
from django.urls import reverse
from users.models import FbUser
from friends.models import Friend
from posts.models import Post
from django.core.files.uploadedfile import SimpleUploadedFile



class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'email':'test@example.com',
            'password':'12345678'
        }
        self.signup_crendentials = {
            'first_name':'test',
            'last_name': 'user',
            'date_of_birth': '2004-02-21',
            'gender': 'Male',
            'email': 'test2@example.com',
            'username':'test12',
            'password': '123456789'
        }
        self.user = FbUser.objects.create_user(username="user34", email=self.credentials['email'], password=self.credentials['password'])

        self.fbuser1 = FbUser.objects.create_user(username="user12", email="user1@example.com", password="12345678")
        self.fbuser2 = FbUser.objects.create_user(username="user21", email="user2@exampl.com", password="12345678")
        self.notfriend = FbUser.objects.create_user(username="randomguy", email="random12@example.com", password="12345678")

        Friend.objects.create(from_friend=self.fbuser1, to_friend=self.fbuser2)
        Friend.objects.create(from_friend=self.fbuser2, to_friend=self.fbuser1)   

        self.post1 = Post.objects.create(author=self.fbuser2, body="demo", image="static/images/Default_pfp.jpg")
        self.post2 = Post.objects.create(author=self.fbuser2, body="demo", image="static/images/Default_pfp.jpg")

    def test_login(self):
        response = self.client.post(reverse('users:login'), self.credentials, follow=True)

        self.assertEqual(response.context['user'],self.user)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_active)
    
    def test_signup(self):
        response = self.client.post(reverse('users:signup'), self.signup_crendentials, follow=True)

        self.assertTrue(FbUser.objects.filter(email=self.signup_crendentials['email']).exists())
    
    def test_home(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.get(reverse("users:home"))

        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        posts = response.context['posts']

        self.assertEqual(user,self.fbuser1)
        self.assertIn(self.post1, posts)
        self.assertIn(self.post2, posts)
    
    def test_logout(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.get(reverse("users:logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:login"))

    def test_search_user(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.post(reverse("users:search_users"), {"searched":"random"})

        self.assertIn(self.notfriend, response.context["users"])
    
    def test_user_profile(self):
        self.client.login(username="user1@example.com", password="12345678")
        post = Post.objects.create(author=self.fbuser1, body="demo3", image="static/images/Default_pfp.jpg")
        response = self.client.get(reverse("users:profile"), follow=True)
        post2 = Post.objects.create(author=self.fbuser2, body="demo4", image="static/images/Default_pfp.png")
        self.assertEqual(response.status_code, 200)
        self.assertIn(post, response.context["liked_dict"])
        self.assertNotIn(post2, response.context["liked_dict"])
    
    def test_upload_profile_picture(self):
        self.client.login(username="user1@example.com", password="12345678")
        image = SimpleUploadedFile("image.jpg", b"randomfilecontent", content_type="image/jpeg")
        response = self.client.post(reverse("users:upload_profile_picture"), {"profile-picture": image},follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:get_profile"))
        self.assertIsNotNone(response.context['user'].profile_picture)


    def test_upload_cover_picture(self):
        self.client.login(username="user1@example.com", password="12345678")
        image = SimpleUploadedFile("image.jpg", b"randomcontent", content_type="image/jpeg")
        response = self.client.post(reverse("users:upload_cover_picture"), {"cover-photo": image}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:get_profile"))
        self.assertIsNotNone(response.context['user'].profile_picture)
    
    def test_upload_bio(self):
        self.client.login(username="user1@example.com", password="12345678")
        response = self.client.post(reverse("users:upload_bio"), {"bio":"test bio"}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:get_profile"))
        self.assertIsNotNone(response.context['user'].bio)
        self.assertEqual(response.context['user'].bio, "test bio")
    
    def test_get_profile(self):
        self.client.login(username="user1@example.com", password="12345678")
        response = self.client.get(reverse("users:get_profile"), follow=True)

        self.assertEqual(response.status_code, 200)
