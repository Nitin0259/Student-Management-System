from django import forms
from .models import StudentsAdd

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentsAdd
        fields = ("__all__")