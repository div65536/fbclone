from django.shortcuts import render
from rest_framework import viewsets
from users.models import FbUser
from posts.models import Post
from .serializers import UserSerializer, PostSerializer, UserRegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import ReadOnlyPermission,EditForObjectAuthor
from rest_framework import generics
# Create your views here.

@api_view(['GET'])
def user_list(request):
    users = FbUser.objects.all()
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    queryset = FbUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ReadOnlyPermission]


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [EditForObjectAuthor]
    serializer_class = PostSerializer

    def create(self, request):
        import pdb
        pdb.set_trace()



class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer