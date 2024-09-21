from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignUpForm

# Create your views here.

def frontpage(request):
    return render(request,'core/frontpage.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request,user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request,'core/signup.html',{'form' : form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('rooms')
        else:
            messages.success(request,("Enter correct username or password"))
            return redirect('login')
    else:
        return render(request,'core/login.html')

def logout_user(request):
    logout(request)
    return redirect('frontpage')
