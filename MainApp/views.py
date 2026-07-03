from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            
            if request.POST.get("remember-me"):
                request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                request.session.set_expiry(0)

            return redirect("dashboard")
        
        messages.error(request, "Invalid username or password")
    return render(request, "login.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect("login")