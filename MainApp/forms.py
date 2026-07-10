from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("__all__")
        widgets = {
            "name": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none",
                "placeholder":"Enter your name"
            }),
            "student_id": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none",
            }),
            "email": forms.EmailInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none",
                "placeholder":"Enter a email"
            }),
            "phone": forms.TextInput(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none",
                "placeholder":"Enter phone number"
            }),
            "courses": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "year": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type":"date",
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "status": forms.Select(attrs={
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "address": forms.Textarea(attrs={
                "rows":4,
                "class":"w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none",
                "placeholder":"Address"
            }),
             "photo": forms.FileInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700"
            }),
        }