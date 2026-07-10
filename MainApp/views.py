from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, AddStudent, Student
from . forms import StudentForm

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
    activitys = Activity.objects.all()[:5]
    recent_students = AddStudent.objects.order_by()[:5]
    return render(request, "dashboard.html", {"user": request.user, "activitys": activitys, "recent_student": recent_students})

def logout_view(request):
    logout(request)
    return redirect("login")

# Filter function
def students(request):
    students = Student.objects.all()
    search = request.GET.get("search")
    course = request.GET.get("course")
    status = request.GET.get("status")

    if search:
        students = students.filter(name__icontains=search)
    if course:
        students = students.filter(course=course)
    if status:
        students = students.filter(status=status)
    return render(request, "student.html", {"students":students})

# Add students on my management
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("students")
    else:
        form = StudentForm()
    
    return render(request, "add_student.html", {"form":form})
