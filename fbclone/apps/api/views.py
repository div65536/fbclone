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
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import EditForObjectAuthor, UserEditPermission
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
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
    @action(detail=True, methods=["POST"],permission_classes=[IsAuthenticated])
    def like(self,request,pk):
        try:
            post = self.get_object()
            already_liked = post.likes.filter(id=request.user.id).exists()
            if already_liked:
                like = post.likes.get(id=request.user.id)
                post.likes.remove(like)
                return Response({"msg":"post unliked"}, status=200)
            else:
                post.likes.add(request.user)
                return Response({"msg":"Post liked"}, status=200)
        except Post.DoesNotExist:
            return Response({"error":"Post not found"}, status=404)
        
        


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

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Comment.objects.none()

        if comment_id:
            try:
                comment = Comment.objects.get(pk=comment_id)
            except Comment.DoesNotExist:
                return Comment.objects.none()
            if comment in post.comments.all():
                return post.comments.filter(id=comment_id)
            else:
                return Comment.objects.none()
        else:
            return post.comments.filter(parent=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user
        serializer.validated_data["post"] = Post.objects.get(
            id=self.kwargs.get("post_id")
        )
        if serializer.validated_data.get("parent") != "":
            parent = serializer.validated_data.get("parent")
            post = Post.objects.get(pk=self.kwargs.get("post_id"))
            if parent not in post.comments.all():
                return Response({"error": "Parent comment does not belong to this post."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class Logout(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=204)
