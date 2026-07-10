from django import forms
from .models import StudentsAdd

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentsAdd
        fields = ("__all__")
        widgets = {
            "name": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "student_id": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "email": forms.EmailInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "phone": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "courses": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "year": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type":"date",
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "status": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "address": forms.Textarea(attrs={
                "rows":4,
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
             "photo": forms.FileInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-slate-300"
            }),
        }