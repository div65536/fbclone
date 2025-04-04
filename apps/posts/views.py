from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm
# Create your views here.

def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postform = PostForm(request.POST,request.FILES)
            print(request.FILES)
            if postform.is_valid():
                instance = postform.save(commit=False)
                instance.author = request.user
                instance.save()
        postform = PostForm()
        return render(request,'posts/create_post.html',{"form":postform})
    else:
        return HttpResponseRedirect(reverse('login'))

def get_posts(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author = request.user)
        print(user_posts)
        return render(request,'posts/posts.html',{"posts":user_posts})