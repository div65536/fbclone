from rest_framework.test import APITestCase, APIClient
from users.models import FbUser
from django.urls import reverse
import json
from posts.models import Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.client.login(username="user1@example.com", password="12345678")

    def test_list_user(self):
       response = self.client.get(reverse("api:user-list"))
       
       self.assertEqual(response.status_code, 200)
    
    def test_detail_user(self):
        response = self.client.get(reverse("api:user-detail", kwargs={"pk":self.user.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_edit_user(self):
        response = self.client.put(reverse("api:user-detail", kwargs={"pk":self.user.id}), {"first_name":"Divyansh","last_name":"Yadav"})
        obj = json.loads(response.content)
        self.assertEqual(obj['first_name'], 'Divyansh')
        self.assertEqual(obj['last_name'], 'Yadav')
    

class TestPostViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.client.login(username="user1@example.com", password="12345678")
        self.post = Post.objects.create(author=self.user, image="static/images/Default_pfp.jpg", body="ok computer")

    def test_list_post(self):
        response = self.client.get(reverse("api:post-list"))

        self.assertEqual(response.status_code, 200)
    
    def test_detail_post(self):
        response = self.client.get(reverse("api:post-detail", kwargs={"pk":self.post.id}))

        self.assertEqual(response.status_code, 200)
    
    def test_edit_post(self):
        response = self.client.put(reverse("api:post-detail", kwargs={"pk":self.post.id}),{"body":"not ok"})
        obj = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj['body'], "not ok")
    
    def test_delete_post(self):
        response = self.client.delete(reverse("api:post-detail", kwargs={"pk":self.post.id}))

        self.assertEqual(response.status_code, 204)
    
    def test_create_post(self):
        image = SimpleUploadedFile("image.jpg", content=open("fbclone/static/images/Default_pfp.jpg", 'rb').read(), content_type="image/jpeg")
        response = self.client.post(reverse("api:post-list"),{"image":image,"body":"ok ok"})

        self.assertEqual(response.status_code, 201)


class TestCommentViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.post = Post.objects.create(author=self.user, image="static/images/Default_pfp.jpg", body="coolcoolcool")
        self.client.login(username="user1@example.com", password="12345678")
        self.comment = Comment.objects.create(author=self.user, post=self.post, content="kun faya kun")
    
    def test_list_comment(self):
        response = self.client.get(reverse("api:comment-list", kwargs={"post_id":self.post.id}))
        
        self.assertEqual(response.status_code, 200)
    
    def test_details_comment(self):
        response = self.client.get(reverse("api:comment-detail", kwargs={"post_id":self.post.id,"pk":self.comment.id}))
        obj = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj['author'], self.user.id)
        self.assertEqual(obj['post'], self.post.id)
        self.assertEqual(obj['content'], "kun faya kun")
    
    def test_edit_comment(self):
        response = self.client.put(reverse("api:comment-detail", kwargs={"post_id":self.post.id,"pk":self.comment.id}), {"content":"Everything in its right place"})
        obj = json.loads(response.content)

        self.assertEqual(obj['content'], "Everything in its right place")
    
    def test_delete_comment(self):
        response = self.client.delete(reverse("api:comment-detail", kwargs={"post_id":self.post.id,"pk":self.comment.id}))
        
        self.assertFalse(Comment.objects.filter(id=self.post.id).exists())
    
    def test_create_comment(self):
        response = self.client.post(reverse("api:comment-list", kwargs={"post_id":self.post.id}), {"content":"okok"})
        obj = json.loads(response.content)

        self.assertEqual(obj['content'],"okok")
        self.assertEqual(obj['parent'], None)
        self.assertEqual(obj['author'], self.user.id)
        self.assertEqual(obj['post'], self.post.id)


class TestLogout(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.client.login(username="user1@example.com", password="12345678")
    def test_logout(self):
        response = self.client.get(reverse("api:logout"))

        self.assertEqual(response.status_code, 204)