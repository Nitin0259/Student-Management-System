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

   

