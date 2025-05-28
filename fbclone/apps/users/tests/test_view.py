from django.test import TestCase, Client
from django.urls import reverse
from users.models import FbUser
from friends.models import Friend
from posts.models import Post
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock


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



    def test_signup_user_already_exits(self):

        signup_crendentials_user_exists = {
            'first_name':'test',
            'last_name': 'user',
            'date_of_birth': '2004-02-21',
            'gender': 'Male',
            'email': 'test121@example.com',
            'username':'test121',
            'password': '123456789'
        }
        FbUser.objects.create_user(username="test121", email="test121@example.com",password="123456789")
        response = self.client.post(reverse('users:signup'), signup_crendentials_user_exists, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(reverse('users:signup'), self.signup_crendentials, follow=True)

        self.assertEqual(response.status_code,200)

    def test_signup_get(self):
        response = self.client.get(reverse('users:signup'), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('users:login'), self.credentials, follow=True)

        self.assertEqual(response.context['user'],self.user)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_active)

    def test_login_incorrect_password(self):
        credentials = {
            "email": "test@example.com",
            "password": "123123123123123"
        }
        response = self.client.post(reverse('users:login'), credentials, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_login_user_does_not_exist(self):
        credentials = {
            "email":"okcomputer@example.com",
            "password":"123123123123"
        }
        response = self.client.post(reverse('users:login'), credentials, follow=True)

        self.assertEqual(response.status_code, 200)

    # def test_signup(self):
    #     response = self.client.post(reverse('users:signup'), self.signup_crendentials, follow=True)

    #     self.assertTrue(FbUser.objects.filter(email=self.signup_crendentials['email']).exists())
    
    def test_home(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.get(reverse("users:home"))

        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        posts = response.context['posts']

        self.assertEqual(user,self.fbuser1)
        self.assertIn(self.post1, posts)
        self.assertIn(self.post2, posts)
    
    def test_home_unauthenticated(self):
        response = self.client.get(reverse("users:home"), follow=True)

        self.assertRedirects(response,reverse("users:login"))

    def test_logout(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.get(reverse("users:logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:login"))

    def test_search_user(self):
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.post(reverse("users:search_users"), {"searched":"random"})

        self.assertIn(self.notfriend, response.context["users"])
    
    def test_search_user_get(self):
        response = self.client.get(reverse("users:search_users"))

        self.assertEqual(response.status_code, 200)

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
        response = self.client.get(reverse("users:get_profile"))
        self.assertEqual(response.status_code, 200)
    
    def test_get_profile_unauth(self):
        response = self.client.get(reverse("users:get_profile"))
        self.assertEqual(response.status_code, 302)

    def test_buy_diamonds(self):
        self.client.login(username="user1@example.com", password="12345678")
        response = self.client.get(reverse("users:buy_diamonds"))
        self.assertEqual(response.status_code, 200)

    def test_buy_diamonds_unauth(self):
        response = self.client.get(reverse("users:buy_diamonds"))
        self.assertEqual(response.status_code, 302)

class TestViewsMocked(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'email': 'test@example.com',
            'password': '12345678'
        }
        self.signup_crendentials = {
            'first_name': 'test',
            'last_name': 'user',
            'date_of_birth': '2004-02-21',
            'gender': 'Male',
            'email': 'test2@example.com',
            'username': 'test12',
            'password': '123456789'
        }

    # @patch("users.views.logger")
    # def test_login_with_real_user(self,mock_logger):
    #     user = FbUser.objects.create_user(email='test@example.com', password='password123', username="test1")
    #     user.is_active = True
    #     user.save()

    #     with patch("users.models.FbUser.objects.get") as mock_get_user:
    #         mock_get_user.return_value = user
    #         with patch("django.contrib.auth.login") as mock_login:
    #             response = self.client.post(reverse("users:login"), {
    #                 'email': 'test@example.com',
    #                 'password': 'password123'
    #             })

    #     self.assertEqual(response.status_code, 302)


    @patch("users.tasks.send_registration_email.delay")
    @patch("users.views.logger")
    @patch("users.models.FbUser.objects.create_user")
    def test_signup_mocked(self, mock_create_user, mock_logger, mock_task):
        mock_user = MagicMock()
        mock_create_user.return_value = mock_user

        response = self.client.post(reverse("users:signup"), self.signup_crendentials)

        mock_logger.info.assert_called()
        mock_task.assert_called()
        self.assertEqual(response.status_code, 200)

    @patch("posts.models.Post")
    def test_profile_post_fetch_mocked(self, mock_post_model):
        FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.client.login(username="user1@example.com", password="12345678")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)

    

    @patch("users.models.FbUser.objects.filter")
    def test_search_user_with_mock(self, mock_user_filter):
        FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.client.login(username="user1@example.com", password="12345678")

        mock_user = MagicMock()
        mock_user.username = "randomguy"
        mock_user_filter.return_value = [mock_user]

        response = self.client.post(reverse("users:search_users"), {"searched": "random"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(mock_user, response.context["users"])