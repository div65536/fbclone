from django.test import TestCase
from posts.models import Post,Comment
from users.models import FbUser

class PostModelTest(TestCase):
    def setUp(self):
        self.user1 = FbUser.objects.create_user(username="user1", email="user1@example.com", password="12345678")
        self.post = Post.objects.create(author=self.user1, image="static/images/Default_pfp.jpg", body="coolcoolcool")
        self.comment = Comment.objects.create(author=self.user1, post=self.post, content="kun faya kun")

    def test_post_model(self):
        self.assertEqual(self.post.body, "coolcoolcool")
        self.assertEqual(self.post.author, self.user1)
        self.assertEqual(self.post.likes.count(),0)
        self.assertIn(self.comment, self.post.comments.all())
        self.assertEqual(self.post.comments.count(),1)
        
    def test_comment_model(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user1)
        self.assertEqual(self.comment.content, "kun faya kun")