from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import logging
logger = logging.getLogger("posts.views")
# Create your views here.


def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            postform = PostForm(request.POST, request.FILES)
            if postform.is_valid():
                instance = postform.save(commit=False)
                instance.author = request.user
                instance.save()
                logger.info(f"User({request.user.email}) uploaded a post")
        postform = PostForm()
        return HttpResponseRedirect(reverse("users:get_profile"))
    else:
        return HttpResponseRedirect(reverse("users:login"))


# def get_posts(request):
#     if request.user.is_authenticated:
#         user_posts = Post.objects.filter(author=request.user)
#         print(user_posts)
#         return render(request, "posts/posts.html", {"posts": user_posts})
#     else:
#         return HttpResponseRedirect(reverse("users:login"))


def handlelike(request, post_id):
    post = Post.objects.get(pk=post_id)
    liked_by = post.likes.all()
    already_liked = post.likes.filter(id=request.user.id).exists()
    if already_liked:
        like = post.likes.get(id=request.user.id)
        post.likes.remove(like)
        logger.info(f"User({request.user.email}) unliked Post({post_id})")
        return HttpResponse(status=409)
    else:
        post.likes.add(request.user)
        logger.info(f"User({request.user.email}) liked Post({post_id})")
        return HttpResponse(status=201)


def handlecomment(request, post_id, parent_id):
    if request.method == "GET":
        post = Post.objects.get(pk=post_id)
        comments = post.get_top_level_nested_comments(parent_id=parent_id)
        info = {}
        for comment in comments:
            info[comment.id] = {
                "content": comment.content,
                "author_name": comment.author.first_name,
                "profile_picture": comment.author.profile_picture.url,
            }
        print(info)
        return JsonResponse(info, status=200, safe=False)
    if request.method == "POST":
        comment_body = request.body.decode("utf-8")
        post = Post.objects.get(pk=post_id)
        author = request.user
        if parent_id == 9999:
            comment = Comment(author=author, post=post, content=comment_body)
        else:
            parent = Comment.objects.get(pk=parent_id)
            comment = Comment(
                author=author, post=post, content=comment_body, parent=parent
            )
        comment.save()
        logger.info(f"User({request.user.email}) Commented on a Post({post_id})")
        info = {}
        if author.profile_picture:
            info["profile_picture"] = author.profile_picture.url
        else:
            info["profile_picture"] = "static/images/Default_pfp.jpg"
        info["first_name"] = author.first_name
        info["comment_id"] = comment.id
        return JsonResponse(info, status=201)


def get_comment_author_info(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    author_info = comment.author.first_name
    author_info = {"first_name": author_info}
    return JsonResponse(author_info, safe=False)


def edit_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        if request.FILES.get("file"):
            post.image = request.FILES["file"]
        post.body = request.POST["text"]
        post.save()
        return HttpResponseRedirect(reverse("users:get_profile"))


def send_stars(request,post_id,amount):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        if request.user.stars >= amount:
            request.user.stars -= amount
            request.user.save()
            post.stars += amount
            post.save()
            return JsonResponse({"msg":"Stars send", "amount":amount}, status=201)
        else:
            return JsonResponse({"msg":"You do not have enough stars", "amount":0}, status=201)