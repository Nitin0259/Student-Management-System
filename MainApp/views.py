from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, Student
from . forms import StudentForm
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth

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

def report_student(request):
    students = Student.objects.all()

    total_student = students.count()
    active_student = students.filter(status="Active").count()
    inactive_student = students.filter(status="Inactive").count()

    course_data = (
        Student.objects
        .values("courses")
        .annotate(total=Count("id"))
        .order_by("courses")
    )

    # Admission-chart

    admission_data = (
        Student.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    ) 

    # Courses_chart
    course_data = (
        Student.objects
        .values("courses")
        .annotate(total=Count("id"))
        .order_by("courses")
    )

    context = {
        "students": students,
        "total_student": total_student,
        "active_student": active_student,
        "inactive_student": inactive_student,
        "course_data": course_data,
        "admission_data": admission_data,
        "course_data": course_data
    }

    return render(request,"reports.html", context)
    
