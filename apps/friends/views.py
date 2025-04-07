from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import FriendRequest,Friend
from users.models import FbUser
# Create your views here.
def send_request(request):
    receiver = FbUser.objects.get(email=request.POST['receiver'])
    try:
        FriendRequest.objects.get(sender=request.user,receiver=receiver)
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=request.user,receiver=receiver)
        friend_request.save()
    return HttpResponse(status=204)


def get_requests(request):
    if request.method=="POST":
        sender = FbUser.objects.get(email=request.POST['sender'])
        obj = FriendRequest.objects.get(sender=sender,receiver=request.user)
        obj.accepted = True
        obj.save()
        friends = Friend(from_friend=sender,to_friend = request.user)
        friends.save()
    query_set = FriendRequest.objects.all().filter(receiver = request.user,accepted=False)
    return render(request,'friends/requests.html',{"requests":query_set})


def get_friends(request):
    query_set1 = Friend.objects.all().filter(from_friend=request.user)
    query_set2 = Friend.objects.all().filter(to_friend=request.user)
    query_set = query_set1.union(query_set2)
    return render(request,"friends/friends.html",{"friends":query_set})
