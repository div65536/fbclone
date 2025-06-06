from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from .models import FbUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from posts.models import Post
from friends.models import Friend
from django.http import HttpResponse
from posts.forms import PostForm
from django.core.mail import send_mail
from fbclone.settings.base import EMAIL_HOST_USER
from .tasks import send_registration_email
from django.views.decorators.cache import never_cache
import requests
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
import stripe
logger = logging.getLogger("users.views")

class HomePageView(TemplateView):
    template_name = 'users/home.html'


class SuccessView(TemplateView):
    template_name = 'users/success.html'


class CancelledView(TemplateView):
    template_name = 'users/cancelled.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    domain_url = 'http://localhost:8000/users/'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            quantity = 1

        price_per_diamond_cents = 100  
        total_amount = price_per_diamond_cents * quantity

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'cancelled/',
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{quantity} Diamond{"s" if quantity > 1 else ""}',
                        },
                        'unit_amount': price_per_diamond_cents,
                    },
                    'quantity': quantity,
                }
            ]
        )
        request.user.stars += quantity
        request.user.save()
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    import pdb
    pdb.set_trace()
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
    
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        
    return HttpResponse(status=200)

def sign_up(request):
    if request.method == "POST":
        logger.info("ok computer")
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.info(request, "Account created successfully!")
            fm.save()
            # send_registration_email.delay(fm.cleaned_data['email'], "Your Account has been succesfully created")
        else:
            messages.info(request, "Account with this email already exists")

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

@never_cache
def home(request):
    if request.user.is_authenticated:
        url = "https://api.weatherstack.com/current?access_key=94ee42c826d70475b2880369e7453a2b"
        latitude= request.GET.get("latitude")
        longitude = request.GET.get("longitude")
        querystring = {"query":f"{latitude},{longitude}"}
        response = requests.get(url, params=querystring)
        data = response.json()
        print(data)
        weather_description = data["current"]["weather_descriptions"][0]
        
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
            {"user": user, "posts": posts, "liked_dict": liked_dict,"weather_description":weather_description},
        )

    else:
        return HttpResponseRedirect(reverse("users:login"))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def search_user(request):
    if request.method == "POST":
        searched = request.POST["searched"] 
        # users = FbUser.objects.filter(email__contains=searched).exclude(
        #     id=request.user.id
        # )
        users = FbUser.objects.filter(email__contains=searched)
        print(users)
        return render(
            request, "users/search_user.html", {"searched": searched, "users": users}
        )
    else:
        return render(request, "users/search_user.html")


def user_profile(request):
    if request.user.is_authenticated:
        form = PostForm()
        user_posts = Post.objects.all().filter(author = request.user).order_by("-created_at")

        liked_dict = {
            post: post.is_liked_by_user(user=request.user) for post in list(user_posts)
        }
        return render(request, "users/profile.html", {"create_post_form":form,"liked_dict":liked_dict})


# def get_feed(request):
#     friendset1 = Friend.objects.values_list("from_friend", flat=True)
#     friendset2 = Friend.objects.values_list("to_friend", flat=True)
#     print(list(friendset1))
#     print(list(friendset2))
#     friendset = friendset1.union(friendset2)
#     posts = (
#         Post.objects.all()
#         .filter(author__in=friendset)
#         .exclude(author=request.user)
#         .order_by("-created_at")
#     )
#     return render(request, "users/feed.html", {"posts": posts})

def get_profile(request):
    if request.user.is_authenticated:
        return render(request,"users/profile.html")
    else:
        return HttpResponseRedirect(reverse("users:login"))


def upload_profile_picture(request):
    request.user.profile_picture = request.FILES['profile-picture']
    request.user.save()
    return HttpResponseRedirect(reverse("users:get_profile"))

def upload_cover_picture(request):
    request.user.cover_photo = request.FILES['cover-photo']
    request.user.save()
    return HttpResponseRedirect(reverse("users:get_profile"))


def upload_bio(request):
    request.user.bio = request.POST["bio"]
    request.user.save()
    return HttpResponseRedirect(reverse("users:get_profile"))

def buy_diamonds(request):
    if request.user.is_authenticated:
        return render(request, "users/buy_diamonds.html")
    else:
        return HttpResponseRedirect(reverse("users:login"))