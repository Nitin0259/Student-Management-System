from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class AddStudent(models.Model):
    GENDER = [('Male','Male'), ('Female','Female')]

    COURSES = [('BCA','BCA'),('B.Tech','B.Tech'),('MCA','MCA'),('BBA','BBA'),('MBA','MBA')]

    student_id = models.CharField(max_length=100, unique=True)
    profile_pic = models.ImageField(upload_to='students/')
    name = models.CharField(max_length=100)
    courses = models.CharField(max_length=100, choices=COURSES)
    year = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=100, choices=GENDER)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
# Seach student
class Student(models.Model):
    GENDER = [('Male','Male'), ('Female','Female')]
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]
    COURSES = [('BCA','BCA'),('B.Tech','B.Tech'),('MCA','MCA'),('BBA','BBA'),('MBA','MBA')]

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    gender = models.CharField(max_length=100, choices=GENDER) 
    courses = models.CharField(max_length=100, choices=COURSES)
    phone = models.CharField(max_length=12)
    semester = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
