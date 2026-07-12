from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, Student
from . forms import StudentForm
from django.db.models import Q

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
    recent_students = Student.objects.order_by("-created_at")[:5]
    return render(request, "dashboard.html", {"user": request.user, "activitys": activitys, "recent_students": recent_students})

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
        students = students.filter(courses=course)
    if status:
        students = students.filter(status=status)
    return render(request, "student.html", {"students":students})

# Add students on my management
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()

            # Add studnet
            Activity.objects.create(
                title=f"{student.name} was added",
                color="green",
                user=request.user
            )
             # Edit student
            Activity.objects.create(
                title=f"{student.name} was updated",
                color="blue",
                user=request.user
            )
            # Delete student
            Activity.objects.create(
                title=f"{student.name} was deleted",
                color="red",
                user=request.user
            )
            return redirect("students")
    else:
        form = StudentForm()
    
    return render(request, "add_student.html", {"form":form})

# Views student

def view_student(request,id):
    student = Student.objects.get(id=id)
    return render(request, "view_student.html", {"student":student})

# Edit student

def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            
            # Edit student details
            Activity.objects.create(
                title=f"{student.name} was updated",
                color="blue",
                user=request.user
            )

            return redirect("students")
    else:
        form = StudentForm(instance=student)

    return render(request, "edit_student.html", {"form":form, "student":student})

def delete_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        # Delete student
        Activity.objects.create(
            title=f"{student.name} was deleted",
            color="red",
            user=request.user
        )

        student.delete()

    return redirect("students")

# Search student
def search_student(request):
    query = request.GET.get("q", "")
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name_icontains=query) |
            Q(student_id_icontains=query) |
            Q(email_icontains=query) |
            Q(phone_icontains=query) |
            Q(courses__icontains=query)
        )
    return render(request, "search_student.html", {"query":query, "students":students})
