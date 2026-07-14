from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, Student
from .forms import StudentForm
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook

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

    # Generate report filter
    
    form_date = request.GET.get("form_date")
    to_date = request.GET.get("to_date")
    course = request.GET.get("course")
    status = request.GET.get("status")

    if form_date:
        students = students.filter(created_at__gte=form_date)

    if to_date:
        students = students.filter(created_at__lte=to_date)

    if course:
        students = students.filter(courses=course)

    if status:
        students = students.filter(status=status)


    total_student = students.count()
    active_student = students.filter(status="Active").count()
    inactive_student = students.filter(status="Inactive").count()


    # Admission-chart

    admission_data = (
        Student.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    ) 

    admission_labels = [
        item["month"].strftime("%b" "%y")
        for item in admission_data
    ]

    admission_values = [
        item["total"]
        for item in admission_data
    ]

    # Courses_chart
    course_data = (
        Student.objects
        .values("courses")
        .annotate(total=Count("id"))
        .order_by("courses")
    )

    course_labels = [
        item["courses"]
        for item in course_data
    ]

    course_values = [
        item["total"]
        for item in course_data
    ]

    context = {
        "students": students,
        "total_student": total_student,
        "active_student": active_student,
        "inactive_student": inactive_student,
        
        "admission_values":admission_values,
        "admission_labels": admission_labels,
    
        "course_labels": course_labels,
        "course_values": course_values
    }

    return render(request,"reports.html", context)
    
# Export-pdf
def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="students_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "Students Report")

    y = 760

    students = Student.objects.all()

    for student in students:
        p.drawString(
            40,
            y,
            f"{student.student_id} | {student.name} | {student.courses} | {student.year} | {student.status}"
        )
        y -= 20

    p.save()

    return response

def export_Excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Students"

    sheet.append([
        "student ID",
        "Name",
        "Course",
        "Year",
        "Email",
        "Phone",
        "Status"
    ])

    students = Student.objects.all()

    for s in students:
        sheet.append([
           s.student_id,
            s.name,
            s.courses,
            s.year,
            s.email,
            s.phone,
            s.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="students.xlsx"'

    workbook.save(response)

    return response
