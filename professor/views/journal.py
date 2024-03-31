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
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]
        location = request.POST["location"]
        student_list = request.POST.getlist("selected-student-id")
        journal_object = Post.objects.create(
            title=title,
            author=request.user,
            content=content,
            type_id=6
        )
        PostPeriod.objects.create(post=journal_object, start_date=start_date, end_date=end_date)
        PostLocation.objects.create(
            post=journal_object,
            location=location
        )
        PostSubjectMapping.objects.create(
            subject_id=subject_id,
            post=journal_object
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
    period_object = PostPeriod.objects.get(post=journal_object)
    student_list = PostUserMapping.objects.filter(post=journal_object).all()
    context = {"subject_id": subject_id, "journal_id": journal_id, "object": journal_object,
               "period_object":period_object,"student_list": student_list, "type_id": 6}
    return render(request, "professor/journal/journal_detail.html", context)
