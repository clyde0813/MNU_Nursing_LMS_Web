from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


def journal(request, subject_id):
    journal_objects = Journal.objects.filter(author=request.user, subject_id=subject_id)
    context = {"subject_id": subject_id, "journal_objects": journal_objects, "type_id": 6}
    return render(request, "professor/journal/journal_list.html", context)


def journal_create(request, subject_id):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        created_date = request.POST["created_date"]
        student_list = request.POST.getlist("selected-student-id")
        journal_object = Journal.objects.create(title=title, content=content, created_date=created_date,
                                                subject_id=subject_id, author=request.user)
        for student_id in student_list:
            JournalStudent.objects.create(journal=journal_object, student_id=student_id)
        return redirect("professor:journal_detail", subject_id, journal_object.id)
    student_objects = Enrollment.objects.filter(subject_id=subject_id, status=True)
    professor_record_objects = Journal.objects.filter(author=request.user)
    context = {
        "subject_id": subject_id,
        "student_objects": student_objects,
        "professor_record_objects": professor_record_objects,
        "type_id": 6
    }
    return render(request, "professor/journal/journal_create.html", context)


def journal_detail(request, subject_id, journal_id):
    journal_object = Journal.objects.get(id=journal_id)
    student_list = JournalStudent.objects.filter(journal=journal_object).all()
    context = {"subject_id": subject_id, "journal_id": journal_id, "object": journal_object,
               "student_list": student_list, "type_id": 6}
    return render(request, "professor/journal/journal_detail.html", context)
