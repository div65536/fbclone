from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
# Create your views here.


def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            postform = PostForm(request.POST, request.FILES)
            print(request.FILES)
            if postform.is_valid():
                instance = postform.save(commit=False)
                instance.author = request.user
                instance.save()
        postform = PostForm()
        return HttpResponse(status=201)
    else:
        return HttpResponseRedirect(reverse("login"))


def get_posts(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author=request.user)
        print(user_posts)
        return render(request, "posts/posts.html", {"posts": user_posts})


def handlelike(request, post_id):
    post = Post.objects.get(pk=post_id)
    liked_by = post.likes.all()
    already_liked = post.likes.filter(id=request.user.id).exists()
    if already_liked:
        like = post.likes.get(id=request.user.id)
        post.likes.remove(like)
        return HttpResponse(status=409)
    else:
        post.likes.add(request.user)
        return HttpResponse(status=201)

def handlecomment(request, post_id, parent_id):
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        comments = post.get_top_level_nested_comments(parent_id=parent_id)
        info={}
        for comment in comments:
            info[comment.id] = {
                "content":comment.content,
                "author_name":comment.author.first_name,
                "profile_picture":comment.author.profile_picture.url
            }
        print(info)
        return JsonResponse(info,status=200,safe=False)
    if request.method == 'POST':
        comment_body = request.body.decode("utf-8")
        post = Post.objects.get(pk=post_id)
        author = request.user
        if parent_id == 9999:
            comment = Comment(author=author, post=post,content=comment_body)
        else:
            parent = Comment.objects.get(pk=parent_id)
            comment = Comment(author=author,post=post,content=comment_body,parent=parent)
        comment.save()
        info = {}
        info["profile_picture"] = author.profile_picture.url
        info["first_name"] = author.first_name
        info["comment_id"] = comment.id
        return JsonResponse(info,status=201)


def get_comment_author_info(request,comment_id):
    comment = Comment.objects.get(pk=comment_id)
    author_info = comment.author.first_name
    author_info = {
    "first_name":author_info
    }
    return JsonResponse(author_info,safe=False)
