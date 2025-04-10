from django.db import models
from users.models import FbUser
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(FbUser,on_delete=models.CASCADE)
    image = models.ImageField(blank = True,upload_to="images/")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.body
    

class Likes(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    liker = models.ForeignKey(FbUser,on_delete=models.CASCADE)

