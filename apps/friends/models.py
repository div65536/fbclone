from django.db import models
from users.models import FbUser
# Create your models here.

class FriendRequest(models.Model):
    sender = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="receiver")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.receiver}'


class Friend(models.Model):
    from_friend = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="from_friend")
    to_friend = models.ForeignKey(FbUser,on_delete=models.CASCADE,related_name="to_friend")

    def __str__(self):
        return f'{self.from_friend}   {self.to_friend}'
    