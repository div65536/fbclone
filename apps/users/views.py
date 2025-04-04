from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import SignUpForm,LoginForm
from django.contrib import messages
from .models import FbUser
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            try:
                FbUser.objects.get(email=fm.cleaned_data['email'])
                messages.info(request,"User with this email already exists!")
            except FbUser.DoesNotExist:
                messages.info(request,"Account created successfully!")
                fm.save()
    else:
        fm = SignUpForm()
    return render(request,'users/signup.html',{"form":fm})

def login_user(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']
            user = authenticate(username=email,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('users:home'))
            else:
                try:
                    user = FbUser.objects.get(email=email)
                    messages.info(request,"Incorrect password")
                except FbUser.DoesNotExist:
                    messages.info(request,"No account with this email exists")

    else:
        loginform = LoginForm()
    return render(request,'users/login.html',{"form":loginform})

def home(request):
    if request.user.is_authenticated:
        user = FbUser.objects.get(email=request.user)
        return render(request,'users/base.html',{"user":user})
    else:
        return HttpResponseRedirect(reverse('users:login'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def search_user(request):
    if request.method == "POST":
        searched = request.POST['searched']
        users = FbUser.objects.filter(email__contains=searched).exclude(id=request.user.id)
        print(users)
        return render(request,'users/search_user.html',{"searched":searched,'users':users})
    else:
        return render(request,'users/search_user.html')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'users/profile.html',{})