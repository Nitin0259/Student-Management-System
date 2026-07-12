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
    
# Student Models
class Student(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]
    COURSES = [('BCA','BCA'),('B.Tech','B.Tech'),('MCA','MCA'),('BBA','BBA'),('MBA','MBA')]

    name = models.CharField(max_length=100)
    email = models.EmailField()

    student_id = models.CharField(max_length=20, unique=True)

    photo = models.ImageField(upload_to="students/", blank=True, null=True)

    courses = models.CharField(max_length=50, choices=COURSES)

    phone = models.CharField(max_length=10)

    year = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES,
        default="1st Year"
    )

    date_of_birth = models.DateField()

    created_at = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"
