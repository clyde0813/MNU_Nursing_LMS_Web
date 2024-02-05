from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


def journal(request, subject_id):
    journal_objects = Post.objects.filter(
        author=request.user,
        postsubjectmapping__subject_id=subject_id,
        type_id=6
    ).all()
    context = {"subject_id": subject_id, "journal_objects": journal_objects, "type_id": 6}
    return render(request, "professor/journal/journal_list.html", context)


def journal_create(request, subject_id):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        created_date = request.POST["created_date"]
        location = request.POST["location"]
        student_list = request.POST.getlist("selected-student-id")
        journal_object = Post.objects.create(
            title=title,
            author=request.user,
            content=content,
            created_date=created_date,
            type_id=6
        )
        PostLocation.objects.create(
            post=journal_object,
            location=location
        )
        for student_id in student_list:
            PostUserMapping.objects.create(post=journal_object, user_id=student_id)
        return redirect("professor:journal_detail", subject_id, journal_object.id)

    student_objects = Enrollment.objects.filter(
        subject_id=subject_id,
        status=True
    )

    professor_record_objects = Post.objects.filter(
        author=request.user,
        postsubjectmapping__subject_id=subject_id,
        type_id=6
    ).all()

    context = {
        "subject_id": subject_id,
        "student_objects": student_objects,
        "professor_record_objects": professor_record_objects,
        "type_id": 6
    }
    return render(request, "professor/journal/journal_create.html", context)


def journal_detail(request, subject_id, journal_id):
    journal_object = Post.objects.get(id=journal_id)
    student_list = PostUserMapping.objects.filter(post=journal_object).all()
    context = {"subject_id": subject_id, "journal_id": journal_id, "object": journal_object,
               "student_list": student_list, "type_id": 6}
    return render(request, "professor/journal/journal_detail.html", context)
