from django.db import models
from users.models import FbUser
# Create your models here.

class FriendRequest(models.Model):
    sender = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="receiver")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


