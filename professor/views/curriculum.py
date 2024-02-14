from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *
import filetype


@login_required(redirect_field_name=None)
def curriculum(request, subject_id, type_id):
    curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=type_id) \
        .order_by("created_date").all()
    type_name = PostType.objects.get(id=type_id).name
    subject_name = Subject.objects.get(id=subject_id).name
    context = {
        "subject_id": subject_id,
        "type_id": type_id,
        "subject_name": subject_name,
        "type_name": type_name,
        "objects": curriculum_objects
    }
    return render(request, "professor/list/list_layout.html", context)


# 커리큘럼 생성
@login_required(redirect_field_name=None)
def curriculum_create(request, subject_id, type_id):
    if request.method == "POST":
        # default
        title = request.POST.get("title")
        content = request.POST.get("content")
        curriculum_object = Post.objects.create(title=title, content=content, author=request.user, type_id=type_id)
        PostSubjectMapping.objects.create(post=curriculum_object, subject_id=subject_id)

        # 평가 여부
        if request.POST.get("eval"):
            evaluation = True if request.POST.get("eval") == "True" else False
            PostEvaluationStatus.objects.create(post=curriculum_object, status=evaluation)

        # 체크리스트
        if request.POST.get("checklist_set_id", default=None):
            checklist_set_id = int(request.POST.get("checklist_set_id", default=None))
            PostChecklistMapping.objects.create(checklist_set_id=checklist_set_id, post=curriculum_object)

        # 기간
        if request.POST.get("period"):
            start_date = request.POST.get("period")
            # end_date = request.POST.get("end_date")
            PostPeriod.objects.create(post=curriculum_object, start_date=start_date)

        if request.POST.get("deadline"):
            deadline = request.POST.get("deadline")
            PostDeadline.objects.create(post=curriculum_object, deadline=deadline)

        # 파일
        if request.FILES.getlist("files"):
            for file in request.FILES.getlist("files"):
                file_object = PostFile.objects.create(post=curriculum_object)
                file_object.file = file
                file_object.filename = file.name
                if filetype.is_image(file):
                    file_object.file_extension = "image"
                elif filetype.is_video(file):
                    file_object.file_extension = "video"
                file_object.save()

        if request.POST.get("location"):
            location = request.POST.get("location")
            PostLocation.objects.create(post=curriculum_object, location=location)
        curriculum_object.save()
        return redirect("professor:curriculum", subject_id, type_id)

    deadline_input_status = False
    evaluation_input_status = False
    checklist_input_status = False
    period_input_status = False
    checklist_objects = None

    # 공지사항
    if type_id == 1:
        pass
    # 지침서
    elif type_id == 2:
        deadline_input_status = True
        evaluation_input_status = False
    # 핵심수기술
    elif type_id == 3:
        deadline_input_status = True
        evaluation_input_status = True
        checklist_input_status = True
        checklist_objects = ChecklistSet.objects.all()
    # 과제
    elif type_id == 4:
        deadline_input_status = True
        evaluation_input_status = True
    # 실습일지
    elif type_id == 5:
        deadline_input_status = True
        evaluation_input_status = True
        period_input_status = True

    context = {
        "subject_id": subject_id,
        "type_id": type_id,
        "subject_name": Subject.objects.get(id=subject_id).name,
        "type_name": PostType.objects.get(id=type_id).name,
        "checklist_objects": checklist_objects,
        "input_list": {
            "title": True,
            "content": True,
            "deadline": deadline_input_status,
            "evaluation": evaluation_input_status,
            "checklist": checklist_input_status,
            "period": period_input_status
        }
    }
    return render(request, "professor/layout/curriculum_submit.html", context)


@login_required(redirect_field_name=None)
def curriculum_modify(request, subject_id, type_id, curriculum_id):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        curriculum_object = Post.objects.get(id=curriculum_id)
        curriculum_object.title = title
        curriculum_object.content = content
        curriculum_object.save()

        # 평가 여부
        if request.POST.get("eval"):
            evaluation = True if request.POST.get("eval") == "True" else False
            tmp_object = PostEvaluationStatus.objects.filter(post=curriculum_object)
            if tmp_object.exists():
                tmp_object = tmp_object.get()
                tmp_object.status = evaluation
                tmp_object.save()
        # 체크리스트
        if request.POST.get("checklist_set_id", default=None):
            checklist_set_id = int(request.POST.get("checklist_set_id", default=None))
            tmp_object = PostChecklistMapping.objects.filter(post=curriculum_object)
            if tmp_object.exists():
                tmp_object = tmp_object.get()
                tmp_object.checklist_set_id = checklist_set_id
                tmp_object.save()
        # 기간
        if request.POST.get("period"):
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            tmp_object = PostPeriod.objects.filter(post=curriculum_object)
            if tmp_object.exists():
                tmp_object = tmp_object.get()
                tmp_object.start_date = start_date
                tmp_object.end_date = end_date
                tmp_object.save()
        return redirect("professor:curriculum_detail", subject_id, type_id, curriculum_id)
    context = curriculum_context(subject_id, type_id, curriculum_id, "modify")
    return render(request, html_return(type_id, "modify"), context)


@login_required(redirect_field_name=None)
def curriculum_delete(request, subject_id, type_id, curriculum_id):
    Post.objects.get(id=curriculum_id).delete()
    return redirect("professor:curriculum", subject_id, type_id)


@login_required(redirect_field_name=None)
def curriculum_detail(request, subject_id, type_id, curriculum_id):
    context = curriculum_context(subject_id=subject_id, type_id=type_id, curriculum_id=curriculum_id, method="detail")
    return render(request, html_return(type_id, "detail"), context)


@login_required(redirect_field_name=None)
def assignment_detail(request, subject_id, type_id, curriculum_id, assignment_id):
    context = assignment_context(request=request, subject_id=subject_id, curriculum_id=curriculum_id, type_id=type_id,
                                 assignment_id=assignment_id)
    return render(request, html_return(type_id, "assignment"), context)


# 핵심수기술 교수 평가
@login_required(redirect_field_name=None)
def assignment_evaluate(request, subject_id, type_id, curriculum_id, student_id):
    checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
    checklist_group = ChecklistGroup.objects.filter(set=checklist_set_object)

    if request.method == "POST":
        for i in checklist_group:
            checklist_record = request.POST.get("check_" + str(i.id))
            if checklist_record is not None:
                checklist_object = ChecklistRecord.objects.filter(post_id=curriculum_id, author=request.user,
                                                                  target_id=student_id, checklist=i)
                if checklist_object.exists():
                    checklist_object = checklist_object.get()
                    checklist_object.record = int(checklist_record)
                    checklist_object.save()
                else:
                    ChecklistRecord.objects.create(
                        post_id=curriculum_id,
                        author=request.user,
                        target_id=student_id,
                        checklist=i,
                        record=int(checklist_record)
                    )
        return redirect("professor:assignment_evaluate", subject_id, type_id, curriculum_id, student_id)
    else:
        checklist_objects = []
        for i in checklist_group:
            checklist_record = ChecklistRecord.objects.filter(
                checklist=i,
                post_id=curriculum_id,
                target_id=student_id,
                author__profile__group__name="professor")
            print(student_id)
            if checklist_record.exists():
                record = checklist_record.get().record
            else:
                record = None
            checklist_objects.append({
                "id": i.id,
                "content": i.checklist.content,
                "record": record
            })

        # 제출 동영상 object
        assignment_object = Post.objects.filter(child_post__parent_post_id=curriculum_id, author_id=student_id)
        video_object = None

        if assignment_object.exists():
            video_object = PostFile.objects.filter(post=assignment_object.get(), file_extension="video")

        if video_object is not None and video_object.exists():
            video_object = video_object.get()

        context = {
            "student_object": User.objects.get(id=student_id),
            "subject_id": subject_id,
            "type_id": type_id,
            "curriculum_id": curriculum_id,
            "student_id": student_id,
            "checklist_objects": checklist_objects,
            "video_object": video_object
        }
        return render(request, html_return(type_id, "evaluate"), context)
