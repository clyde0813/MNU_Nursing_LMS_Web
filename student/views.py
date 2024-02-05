from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models.models import *
from function.student.curriculum import *
from function.student.html import *


def get_student_enrollments(student):
    all_enrollments = Enrollment.objects.filter(student=student)
    active_enrollments = all_enrollments.filter(status=True).order_by('-id')
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
    curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=type_id) \
        .order_by("created_date").all()
    type_name = PostType.objects.get(id=type_id).name
    subject_name = Subject.objects.get(id=subject_id).name
    context = {"subject_id": subject_id, "type_id": type_id, "subject_name": subject_name, "type_name": type_name,
               "objects": curriculum_objects}
    return render(request, "student/list/list_layout.html", context)


@login_required(redirect_field_name=None)
def curriculum_detail(request, subject_id, type_id, curriculum_id):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        assignment = Post.objects.create(
            title=title,
            content=content,
            type_id=7,
            author=request.user
        )

        PostPostMapping.objects.create(
            parent_post_id=curriculum_id,
            child_post=assignment
        )

        if type_id == 3:
            checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
            checklist_group = ChecklistGroup.objects.filter(set=checklist_set_object)
            for i in checklist_group:
                checklist_record = request.POST.get("check_" + str(i.id))
                if checklist_record is not None:
                    ChecklistRecord.objects.create(
                        post_id=curriculum_id,
                        author=request.user,
                        checklist=i,
                        target=request.user,
                        record=int(checklist_record)
                    )
            # 영상 저장
            file = request.FILES.get("video-file")
            file_object = PostFile.objects.create(post=assignment)
            file_object.file = file
            file_object.filename = file.name
            file_object.file_extension = "video"
            file_object.save()
        elif type_id == 5:
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            PostPeriod.objects.create(post=assignment, start_date=start_date, end_date=end_date)
        return redirect("student:curriculum_detail", subject_id, type_id, curriculum_id)
    else:
        if type_id == 1 or Post.objects.filter(child_post__parent_post_id=curriculum_id, author=request.user).exists():
            method = "detail"
        else:
            method = "create"
        context = curriculum_context(request=request, subject_id=subject_id, curriculum_id=curriculum_id,
                                     type_id=type_id, method=method)
        return render(request, html_return(type_id, method), context)


@login_required(redirect_field_name=None)
def enrollment(request, subject_id):
    if not Enrollment.objects.filter(subject_id=subject_id, student=request.user).exists():
        Enrollment.objects.create(subject_id=subject_id, student=request.user, status=False, confirmed_date=None)
    return redirect("common:index")
