from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


def journal(request, subject_id):
    context = {"subject_id": subject_id, "type_id": 6}
    return render(request, "professor/journal/journal_list.html", context)


def journal_create(request, subject_id):
    student_objects = Enrollment.objects.filter(subject_id=subject_id, status=True)
    context = {"subject_id": subject_id, "student_objects": student_objects, "type_id": 6}
    return render(request, "professor/journal/journal_create.html", context)
