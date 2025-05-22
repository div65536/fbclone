from rest_framework import serializers
from users.models import FbUser
from posts.models import Post, Comment
from django.contrib.auth.hashers import make_password


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "created_at", "post", "parent", "content", "replies"]
        read_only_fields = [
            "author",
            "post",
        ]

    def get_replies(self, obj):
        return CommentSerializer(Comment.objects.filter(parent=obj), many=True).data


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "image", "body", "created_at", "comments"]
        read_only_fields = ["author"]

    def get_comments(self, obj):
        return CommentSerializer(obj.get_top_level_comments(), many=True).data


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = FbUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "profile_picture",
        ]
        read_only_fields = ["email"]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            request = self.context.get("request")
            absolute_path = request.build_absolute_uri(obj.profile_picture.url)
            return absolute_path
        else:
            return "No Profile Picture"


class UserRegistrationSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=(("Male", "Male"), ("Female", "Female")))

    class Meta:
        model = FbUser
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "email",
            "username",
            "password",
        ]
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'date_of_birth': {'required': True},
                        'gender': {'required': True},
                        'email': {'required': True},
                        'username': {'required': True},
                        'password': {'required': True, 'write_only': True}
                        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
