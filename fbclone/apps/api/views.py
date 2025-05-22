from rest_framework import viewsets
from users.models import FbUser
from posts.models import Post, Comment
from .serializers import (
    UserSerializer,
    PostSerializer,
    UserRegistrationSerializer,
    CommentSerializer,
)

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import EditForObjectAuthor, UserEditPermission
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import logout
# from rest_framework.authentication import TokenAuthentication


# @api_view(['GET'])
# def user_list(request):
#     users = FbUser.objects.all()
#     serializer = UserSerializer(users, many=True, context={'request': request})
#     return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    queryset = FbUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserEditPermission]


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [EditForObjectAuthor]
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [EditForObjectAuthor, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("pk")
        if comment_id and post_id:
            return Post.objects.get(id=post_id).comments.filter(id=int(comment_id))
        return Post.objects.get(id=post_id).get_top_level_comments()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user
        serializer.validated_data["post"] = Post.objects.get(
            id=self.kwargs.get("post_id")
        )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class Logout(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=204)
