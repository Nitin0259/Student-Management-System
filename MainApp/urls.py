from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name='login'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("students/", views.students, name='students'),
    path("students/add/", views.add_student, name='add_student')
]