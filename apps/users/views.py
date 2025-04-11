from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from .models import FbUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from posts.models import Post
from friends.models import Friend

# Create your views here.


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            try:
                FbUser.objects.get(email=fm.cleaned_data["email"])
                messages.info(request, "User with this email already exists!")
            except FbUser.DoesNotExist:
                messages.info(request, "Account created successfully!")
                fm.save()
    else:
        fm = SignUpForm()
    return render(request, "users/signup.html", {"form": fm})


def login_user(request):
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data["email"]
            password = loginform.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("users:home"))
            else:
                try:
                    user = FbUser.objects.get(email=email)
                    messages.info(request, "Incorrect password")
                except FbUser.DoesNotExist:
                    messages.info(request, "No account with this email exists")

    else:
        loginform = LoginForm()
    return render(request, "users/login.html", {"form": loginform})


def home(request):
    if request.user.is_authenticated:
        user = FbUser.objects.get(email=request.user)
        friendset1 = Friend.objects.values_list("from_friend", flat=True).filter(
            to_friend=request.user
        )
        friendset2 = Friend.objects.values_list("to_friend", flat=True).filter(
            from_friend=request.user
        )
        friendset = friendset1.union(friendset2)
        posts = (
            Post.objects.all()
            .filter(author__in=friendset)
            .exclude(author=request.user)
            .order_by("-created_at")
        )
        liked_dict = {
            post: post.is_liked_by_user(user=request.user) for post in list(posts)
        }
        print(liked_dict)
        return render(
            request,
            "users/base.html",
            {"user": user, "posts": posts, "liked_dict": liked_dict},
        )
    else:
        return HttpResponseRedirect(reverse("users:login"))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def search_user(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        users = FbUser.objects.filter(email__contains=searched).exclude(
            id=request.user.id
        )
        print(users)
        return render(
            request, "users/search_user.html", {"searched": searched, "users": users}
        )
    else:
        return render(request, "users/search_user.html")


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "users/profile.html", {})


def get_feed(request):
    friendset1 = Friend.objects.values_list("from_friend", flat=True)
    friendset2 = Friend.objects.values_list("to_friend", flat=True)
    print(list(friendset1))
    print(list(friendset2))
    friendset = friendset1.union(friendset2)
    posts = (
        Post.objects.all()
        .filter(author__in=friendset)
        .exclude(author=request.user)
        .order_by("-created_at")
    )
    return render(request, "users/feed.html", {"posts": posts})
