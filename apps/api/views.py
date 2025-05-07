from django.shortcuts import render
from rest_framework import viewsets
from users.models import FbUser
from posts.models import Post
from .serializers import UserSerializer, PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def user_list(request):
    users = FbUser.objects.all()
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    queryset = FbUser.objects.all()
    serializer_class = UserSerializer


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer