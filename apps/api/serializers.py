from rest_framework import serializers
from users.models import FbUser
from posts.models import Post
from django.contrib.auth.hashers import make_password

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'image', 'body', 'created_at']
        read_only_fields = ['author']




class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = FbUser
        fields = ["id", "first_name", "last_name", "email", "date_of_birth", "profile_picture"]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            absolute_path = request.build_absolute_uri(obj.profile_picture.url)
            return absolute_path
        else:
            return "No Profile Picture"
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=(("Male", "Male"), ("Female", "Female")))

    class Meta:
        model = FbUser
        fields = ["first_name", "last_name", "date_of_birth", "gender", "email", "username", "password"]
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = FbUser(**validated_data)
        user.save()
        return user