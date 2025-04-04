from django.db import models
from users.models import FbUser
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(FbUser,on_delete=models.CASCADE)
    image = models.ImageField(blank = True,upload_to="images/")
    body = models.TextField()

    def __str__(self):
        return self.body