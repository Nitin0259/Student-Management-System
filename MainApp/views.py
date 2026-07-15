from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, Student, Settings
from .forms import StudentForm, SettingsForm
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.contrib.auth import update_session_auth_hash

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

    students = Student.objects.all()
    total_students = students.count()
    active_students = students.filter(status="Active").count()
    inactive_students = students.filter(status="Inactive").count()
    total_courses = students.values("courses").distinct().count()
    filter_type = request.GET.get("filter", "year")

    # Year
    if filter_type == "year":
        students = Student.objects.filter(
        created_at__year=timezone.now().year
        )
    
    # Month
    elif filter_type == "month":
        today = timezone.now()

        students = Student.objects.filter(
            created_at__year = today.year,
            created_at__month = today.month
        )
    
    # 6 Month
    elif filter_type == "6month":
        six_month_ago = timezone.now() - timedelta(days=180)

        students = Student.objects.filter(
            created_at__gte = six_month_ago
        )
    
    else:
        students = Student.objects.all()

    # Dashboard admission chart
    admission_data = (
        students
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

    # Dashboard course chart
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
    "user": request.user,
    "activitys": activitys,
    "recent_students": recent_students,

    "total_students": total_students,
    "active_students": active_students,
    "inactive_students": inactive_students,
    "total_courses": total_courses,

    "admission_labels": admission_labels,
    "admission_values": admission_values,
    "filter": filter_type,

    "course_labels": course_labels,
    "course_values": course_values,

}

    return render(request, "dashboard.html", context)

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

        settings, created = Settings.objects.get_or_create(user=request.user)

        if form.is_valid():
            student = form.save()

        if settings.notifications:
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

    settings, created = Settings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            
        if settings.notifications:
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

    settings, created = Settings.objects.get_or_create(user=request.user)

    if request.method == "POST":

        if settings.notifications:
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
    total_courses = students.values("courses").distinct().count()


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
        "total_courses": total_courses,
        
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


# Settings
@login_required
def settings(request):

    settings, created = Settings.objects.get_or_create(user=request.user)

    current_password = request.POST.get("current_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")

    if current_password and new_password and confirm_password:
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")

        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")

        else:
            request.user.set_password(new_password)
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, "Password changed successfully.")


    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        form = SettingsForm(request.POST, request.FILES,instance=settings)

        if form.is_valid():
            settings = form.save(commit=False)

            settings.notifications = "notifications" in request.POST
            settings.save()
            form.save()

            messages.success(request,"Settings updated successfully.")
            return redirect("settings")

    else:

        form = SettingsForm(instance=settings)

    return render(request,"setting.html", {"form": form, "settings":settings})


# Delete all student
@login_required
def delete_all_student(request):
    if request.method == "POST":
        total = Student.objects.count()

        Student.objects.all().delete()

        settings, created = Settings.objects.get_or_create(user=request.user)

        if settings.notifications:
            Activity.objects.create(
                title=f"Deleted all students ({total})",
                color="red",
                user=request.user
            )
        
        messages.success(request, "All students deleted successfully.")

    return redirect("settings")