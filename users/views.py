from django.shortcuts import render,HttpResponse
from .forms import SignUpForm,LoginForm
from django.contrib import messages
from .models import FbUser
from django.contrib.auth import authenticate,login,logout
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

def login(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            try:
                user = FbUser.objects.get(email=loginform.cleaned_data['email'])
                if user.password == loginform.cleaned_data['password']:
                    messages.info(request,"Login successfull")
                else:
                    messages.info(request,"Password is wrong!")
            except User.DoesNotExist:
                messages.info(request,"Account with this email does not exist!")
    else:
        loginform = LoginForm()
    return render(request,'users/login.html',{"form":loginform})