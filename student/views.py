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
    objects = []
    for data in curriculum_objects:
        status = False
        if Post.objects.filter(child_post__parent_post=data, author=request.user).exists():
            status = True
        objects.append({
            "object": data,
            "status": status
        })
    context = {"subject_id": subject_id, "type_id": type_id, "subject_name": subject_name, "type_name": type_name,
               "objects": objects}
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
        if request.FILES.get("file"):
            file = request.FILES["file"]
            PostFile.objects.create(post=assignment, file=file, filename=file.name, file_extension="assignment")

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
            start_date = request.POST.get("date")
            # end_date = request.POST.get("end_date")
            PostPeriod.objects.create(post=assignment, start_date=start_date)
        return redirect("student:curriculum_detail", subject_id, type_id, curriculum_id)

    else:
        if type_id == 1 \
                or type_id == 8 \
                or Post.objects.filter(child_post__parent_post_id=curriculum_id, author=request.user).exists():
            method = "detail"
        else:
            method = "create"

        curriculum_object = Post.objects.get(id=curriculum_id)
        file_objects = curriculum_object.postfile_set.all()
        context = None

        if type_id not in [1, 8] and method == "detail":
            assignment_object = Post.objects.get(child_post__parent_post_id=curriculum_id, author=request.user)
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object, "assignment_object": assignment_object,
                "files": file_objects, "video": None
            }

            if type_id == 3:
                checklist_objects = []
                checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
                checklist_group_object = ChecklistGroup.objects.filter(set=checklist_set_object)
                for i in checklist_group_object:
                    checklist_record = ChecklistRecord.objects.filter(author=request.user, checklist=i,
                                                                      post_id=curriculum_id, target=request.user)
                    if checklist_record.exists():
                        record = checklist_record.get().record
                    else:
                        record = None
                    checklist_objects.append({
                        "id": i.id,
                        "content": i.checklist.content,
                        "record": record
                    })
                if PostFile.objects.filter(post=assignment_object, file_extension="video").exists():
                    context["video"] = PostFile.objects.filter(post=assignment_object, file_extension="video").get()
                context["checklist_objects"] = checklist_objects

        if type_id == 1:
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object, "files": file_objects,
            }
        elif type_id in [2, 4, 5]:
            if method == "create":
                type_name = curriculum_object.type.name
                context = {
                    "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                    "object": curriculum_object, "files": file_objects,
                }
        elif type_id == 3:
            if method == "create":
                checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
                checklist_objects = ChecklistGroup.objects.filter(set=checklist_set_object)
                type_name = curriculum_object.type.name
                context = {
                    "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                    "object": curriculum_object, "checklist_objects": checklist_objects, "files": file_objects
                }
        # 학생 평가
        elif type_id == 8:
            checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
            checklist_objects = ChecklistGroup.objects.filter(set=checklist_set_object)
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object, "checklist_objects": checklist_objects, "files": file_objects,
            }

        return render(request, html_return(type_id, method), context)


@login_required(redirect_field_name=None)
def enrollment(request, subject_id):
    if not Enrollment.objects.filter(subject_id=subject_id, student=request.user).exists():
        Enrollment.objects.create(subject_id=subject_id, student=request.user, status=False, confirmed_date=None)
    return redirect("common:index")
