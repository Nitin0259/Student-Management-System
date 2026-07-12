from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name='login'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("students/", views.students, name='students'),
    path("add_student/", views.add_student, name='add_student'),
    path("student/<int:id>/", views.view_student, name="view_student"),
    path("student/edit/<int:id>/", views.edit_student, name="edit_student"),
    path("student/delete/<int:id>/", views.delete_student, name="delete_student"),
    path("search/", views.search_student, name='search_student'),
]