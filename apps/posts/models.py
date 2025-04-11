from django.db import models
from users.models import FbUser


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(FbUser, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="images/")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        "users.FbUser", related_name="liked_posts", null=True, blank=True
    )

    def __str__(self):
        return self.body

    def is_liked_by_user(self, user):
        return self.likes.filter(id=user.id).exists()


class Comment(models.Model):
    author = models.ForeignKey(
        FbUser, related_name="comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
