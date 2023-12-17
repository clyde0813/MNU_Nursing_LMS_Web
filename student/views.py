from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models.models import *
from function.student.curriculum import *
from function.student.html import *


def get_student_enrollments(student):
    all_enrollments = Enrollment.objects.filter(student=student)
    active_enrollments = all_enrollments.order_by('-id')
    pending_enrollments = all_enrollments.filter(status=False)
    return all_enrollments, active_enrollments, pending_enrollments


@login_required(redirect_field_name=None)
def index(request):
    subjects = Subject.objects.all()
    all_enrolls, active_enrolls, pending_enrolls = get_student_enrollments(request.user)
    subject_enrollments = []

    for subject in subjects:
        if not all_enrolls.filter(subject=subject).exists():
            subject_enrollments.append({
                "id": subject.id,
                "name": subject.name,
                "professor": subject.professor.profile.name
            })

    context = {
        "subject_enrollment_objects": subject_enrollments,
        "enrollment_awaiting_objects": pending_enrolls,
        "enrollment_objects": active_enrolls
    }

    return render(request, "student/subject/list.html", context)


@login_required(redirect_field_name=None)
def curriculum(request, subject_id, type_id):
    curriculum_objects = Curriculum.objects.filter(subject_id=subject_id, type_id=type_id) \
        .order_by("created_date").all()
    type_name = CurriculumType.objects.get(id=type_id).name
    subject_name = Subject.objects.get(id=subject_id).name
    context = {"subject_id": subject_id, "type_id": type_id, "subject_name": subject_name, "type_name": type_name,
               "objects": curriculum_objects}
    return render(request, "student/list/list_layout.html", context)


@login_required(redirect_field_name=None)
def curriculum_detail(request, subject_id, type_id, curriculum_id):
    if request.method == "POST":
        assignment_create(request, subject_id, type_id, curriculum_id)
        return redirect("student:curriculum_detail", subject_id, type_id, curriculum_id)
    else:
        if type_id == 1 or Assignment.objects.filter(curriculum_id=curriculum_id, author=request.user).exists():
            method = "detail"
        else:
            method = "create"
        context = curriculum_context(request=request, subject_id=subject_id, curriculum_id=curriculum_id,
                                     type_id=type_id, method=method)
        return render(request, html_return(type_id, method), context)


@login_required(redirect_field_name=None)
def enrollment(request, subject_id):
    Enrollment.objects.create(subject_id=subject_id, student=request.user)
    return redirect("common:index")
