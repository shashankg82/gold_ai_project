from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Password do not match")
            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")
        

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created! Please login.")
        return redirect("login")
    
    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect("chat_page") #later it will be changed to chat page
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
        

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def chat_view(request):
    return HttpResponse("Welcome to Chat! Only logged-in users can see this.")
