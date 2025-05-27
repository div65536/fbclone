from django.shortcuts import render, HttpResponse
from .models import FriendRequest, Friend
from users.models import FbUser
import logging
logger = logging.getLogger('friends.views')

# Create your views here.
def send_request(request):
    receiver = FbUser.objects.get(email=request.POST["receiver"])
    try:
        FriendRequest.objects.get(sender=request.user, receiver=receiver)
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=request.user, receiver=receiver)
        friend_request.save()
        logger.info(f"User({request.user.email}) sent a friend request to User({receiver.email})")
    return HttpResponse(status=204)


def get_requests(request):
    if request.method == "POST":
        sender = FbUser.objects.get(email=request.POST["sender"])
        obj = FriendRequest.objects.get(sender=sender, receiver=request.user)
        obj.accepted = True
        obj.save()
        friends1 = Friend(from_friend=sender, to_friend=request.user)
        friends2 = Friend(from_friend=request.user, to_friend=sender)
        friends2.save()
        friends1.save()
    query_set = FriendRequest.objects.all().filter(
        receiver=request.user, accepted=False
    )
    return render(request, "friends/requests.html", {"requests": query_set})


def get_friends(request):
    query_set = Friend.objects.filter(from_friend=request.user)
    return render(request, "friends/friends.html", {"friends": query_set})


