from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


@login_required(redirect_field_name=None)
def curriculum(request, subject_id, type_id):
    curriculum_objects = Curriculum.objects.filter(subject_id=subject_id, type_id=type_id) \
        .order_by("created_date").all()
    type_name = CurriculumType.objects.get(id=type_id).name
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
        curriculum_object = Curriculum.objects.create(subject_id=subject_id, type_id=type_id, title=title,
                                                      content=content)

        # 평가 여부
        if request.POST.get("eval"):
            evaluation = True if request.POST.get("eval") == "True" else False
            curriculum_object.eval_status = evaluation
        # 체크리스트
        if request.POST.get("checklist_set_id", default=None):
            checklist_set_id = int(request.POST.get("checklist_set_id", default=None))
            ChecklistCurriculum.objects.create(curriculum=curriculum_object, checklist_set_id=checklist_set_id)
        # 기간
        if request.POST.get("period"):
            period = request.POST.get("period")
            Period.objects.create(curriculum=curriculum_object, date=period)
        # 파일
        if request.FILES.getlist("files"):
            for file in request.FILES.getlist("files"):
                file_object = CurriculumFile.objects.create(curriculum=curriculum_object)
                file_object.file = file
                file_object.filename = file.name
                file_object.save()

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
        evaluation_input_status = True
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
        "type_name": CurriculumType.objects.get(id=type_id).name,
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
        curriculum_modify_func(request, type_id, curriculum_id)
        return redirect("professor:curriculum_detail", subject_id, type_id, curriculum_id)
    context = curriculum_context(subject_id, type_id, curriculum_id, "modify")
    return render(request, html_return(type_id, "modify"), context)


@login_required(redirect_field_name=None)
def curriculum_delete(request, subject_id, type_id, curriculum_id):
    Curriculum.objects.get(id=curriculum_id).delete()
    return redirect("professor:curriculum", subject_id, type_id)


@login_required(redirect_field_name=None)
def curriculum_detail(request, subject_id, type_id, curriculum_id):
    context = curriculum_context(subject_id, type_id, curriculum_id, "detail")
    return render(request, html_return(type_id, "detail"), context)


@login_required(redirect_field_name=None)
def assignment_detail(request, subject_id, type_id, curriculum_id, assignment_id):
    context = assignment_context(request=request, subject_id=subject_id, curriculum_id=curriculum_id, type_id=type_id,
                                 assignment_id=assignment_id)
    return render(request, html_return(type_id, "assignment"), context)


@login_required(redirect_field_name=None)
def assignment_evaluate(request, subject_id, type_id, curriculum_id, assignment_id):
    if request.method == "POST":
        checklist_set_object = ChecklistCurriculum.objects.get(curriculum_id=curriculum_id).checklist_set
        checklist_group = ChecklistGroup.objects.filter(set=checklist_set_object)
        for i in checklist_group:
            checklist_record = request.POST.get("check_" + str(i.id))
            if checklist_record is not None:
                checklist_object = ChecklistRecord.objects.filter(assignment_id=assignment_id, author=request.user,
                                                                  checklist=i)
                if checklist_object.exists():
                    checklist_object = checklist_object.get()
                    checklist_object.record = int(checklist_record)
                    checklist_object.save()
                else:
                    ChecklistRecord.objects.create(assignment_id=assignment_id, author=request.user, checklist=i,
                                                   record=int(checklist_record))
        return redirect("professor:assignment_evaluate", subject_id, type_id, curriculum_id, assignment_id)
    else:
        context = evaluation_context(request=request, subject_id=subject_id, curriculum_id=curriculum_id,
                                     type_id=type_id, assignment_id=assignment_id)
        return render(request, html_return(type_id, "evaluate"), context)
