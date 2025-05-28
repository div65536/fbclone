from django.test import TestCase,Client
from django.urls import reverse
from users.models import FbUser
from posts.models import Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user2 = FbUser.objects.create_user(first_name="user2", last_name="test", username="user2", email="user2@example.com",password="12345678")
        self.user = FbUser.objects.create_user(first_name="user", last_name="test", username="user1", email="user@example.com", password="12345678",profile_picture="static/images/Default_pfp.jpg")
        self.image = SimpleUploadedFile("image.jpg", content=open("fbclone/static/images/Default_pfp.jpg", 'rb').read(), content_type="image/jpeg")
        self.post = {
            "image":self.image,
            "body":"coolcoolcool"
        }
        self.dbpost = Post.objects.create(author=self.user, image="static/images/Default_pfp.jpg", body="coolcoolcool")
        self.comment2 = Comment.objects.create(author=self.user, post=self.dbpost,content="ok ok ok")
        self.alreadyliked = Post.objects.create(author=self.user, image="static/images/Default_pfp.jpg", body="coolcoolcool2")
        self.alreadyliked.likes.add(self.user)
        self.comment = Comment.objects.create(author=self.user, post=self.alreadyliked, content="kun faya kun")
        self.comment2 = Comment.objects.create(author=self.user, post=self.alreadyliked, content="kun faya kun", parent=self.comment)

    def test_create_post_unauthenticated(self):
        response = self.client.post(reverse("posts:create_post"), self.post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login"))
    
    def test_create_post_authenticated(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.post(reverse("posts:create_post"), self.post)

        self.assertRedirects(response, reverse("users:get_profile"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.posts.all().count(),3)
    
    def test_handle_like(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.post(reverse("posts:handlelike", kwargs={'post_id':self.dbpost.id}))

        self.assertEqual(self.dbpost.likes.count(),1)

    def test_handle_already_liked(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.post(reverse("posts:handlelike", kwargs={'post_id':self.alreadyliked.id}))

        self.assertEqual(self.alreadyliked.likes.count(),0)

    def test_handle_comment_get(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.get(reverse("posts:handlecomment", kwargs={'post_id':self.alreadyliked.id,'parent_id':self.comment.id}))
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{})
    
    def test_handle_comment_post(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.post(reverse("posts:handlecomment", kwargs={'post_id':self.alreadyliked.id, 'parent_id':9999}))
        response = self.client.post(reverse("posts:handlecomment", kwargs={'post_id':self.alreadyliked.id, 'parent_id':self.comment.id}))
        self.assertEqual(response.status_code, 201)

    def test_get_comment_author_info(self):
        self.client.login(username="user@example.com", password="12345678")
        response = self.client.get(reverse("posts:commentauthorinfo", kwargs={'comment_id':self.comment.id}))

        self.assertEqual(response.content, b'{"first_name": "User"}')
    
    def test_edit_post(self):
        self.client.login(username="user@example.com", password="12345678")
        image = SimpleUploadedFile("image.jpg", content=open("fbclone/static/images/Default_pfp.jpg", 'rb').read(), content_type="image/jpeg")
        response = self.client.post(reverse("posts:edit_post", kwargs={"post_id":self.alreadyliked.id}), {"file":image,"text":"kid A"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:get_profile"))


    def test_handle_comment_post2(self):
        self.client.login(username="user2@example.com", password="12345678")
        response = self.client.post(reverse("posts:handlecomment", kwargs={'post_id':self.alreadyliked.id, 'parent_id':9999}))
        response = self.client.post(reverse("posts:handlecomment", kwargs={'post_id':self.alreadyliked.id, 'parent_id':self.comment.id}))
        self.assertEqual(response.status_code, 201)


