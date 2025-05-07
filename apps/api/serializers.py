from rest_framework import serializers
from users.models import FbUser
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    posts = PostSerializer(many=True)
    
    class Meta:
        model = FbUser
        fields = ["first_name", "last_name", "email", "date_of_birth", "profile_picture", "posts"]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            absolute_path = request.build_absolute_uri(obj.profile_picture.url)
            return absolute_path
        else:
            return "No Profile Picture"
    
    def get_posts(self, obj):
        posts = Post.objects.get(author=obj)
        return PostSerializer(posts, many=True).data