from models.models import *


def curriculum_create_func(request, subject_id, type_id):
    title = request.POST.get("title")
    content = request.POST.get("content")
    curriculum_object = Curriculum.objects.create(subject_id=subject_id, type_id=type_id, title=title, content=content)
    if type_id == 1:
        pass
    if type_id == 2:
        evaluation = True if request.POST.get("eval") == "True" else False
        Evaluation.objects.create(curriculum=curriculum_object, status=evaluation)
    if type_id == 3:
        evaluation = True if request.POST.get("eval") == "True" else False
        checklist_set_id = int(request.POST.get("checklist_set_id", default=None))
        Evaluation.objects.create(curriculum=curriculum_object, status=evaluation)
        ChecklistCurriculum.objects.create(curriculum=curriculum_object, checklist_set_id=checklist_set_id)
    if type_id == 4:
        evaluation = True if request.POST.get("eval") == "True" else False
        Evaluation.objects.create(curriculum=curriculum_object, status=evaluation)
    if type_id == 5:
        evaluation = True if request.POST.get("eval") == "True" else False
        period = request.POST.get("period")
        Evaluation.objects.create(curriculum=curriculum_object, status=evaluation)
        Period.objects.create(curriculum=curriculum_object, date=period)


def curriculum_modify_func(request, type_id, curriculum_id):
    curriculum_object = Curriculum.objects.get(id=curriculum_id)
    curriculum_object.title = request.POST.get("title")
    curriculum_object.content = request.POST.get("content")
    curriculum_object.save()
    if type_id == 1:
        pass
    if type_id == 2:
        evaluation = True if request.POST.get("eval") == "True" else False
        evaluation_object = Evaluation.objects.get(curriculum=curriculum_object)
        evaluation_object.status = evaluation
        evaluation_object.save()
    if type_id == 3:
        evaluation = True if request.POST.get("eval") == "True" else False
        checklist_set_id = request.POST.get("checklist_set_id")
        evaluation_object = Evaluation.objects.get(curriculum=curriculum_object)
        evaluation_object.status = evaluation
        evaluation_object.save()
        checklist_curriculum_object = ChecklistCurriculum.objects.get(curriculum=curriculum_object)
        checklist_curriculum_object.checklist_set_id = checklist_set_id
        checklist_curriculum_object.save()
    if type_id == 4:
        evaluation = True if request.POST.get("eval") == "True" else False
        evaluation_object = Evaluation.objects.get(curriculum=curriculum_object)
        evaluation_object.status = evaluation
        evaluation_object.save()
    if type_id == 5:
        evaluation = True if request.POST.get("eval") == "True" else False
        period = request.POST.get("period")
        evaluation_object = Evaluation.objects.get(curriculum=curriculum_object)
        evaluation_object.status = evaluation
        evaluation_object.save()
        period_object = Period.objects.get(curriculum=curriculum_object)
        period_object.date = period
        period_object.save()


def curriculum_context(subject_id, type_id, curriculum_id, method):
    curriculum_object = None
    if curriculum_id is not None:
        curriculum_object = Curriculum.objects.get(id=curriculum_id)

    if type_id != 1 and method == "detail":
        student_objects = []
        for obj in Enrollment.objects.filter(subject_id=subject_id):
            assignment_object = Assignment.objects.filter(curriculum=curriculum_object, author=obj.student)
            if assignment_object.exists():
                assignment_id = assignment_object.get().id
                assignment_date = assignment_object.get().created_date
            else:
                assignment_id = None
                assignment_date = None
            student_objects.append({
                "id": assignment_id,
                "student": obj.student,
                "assignment_date": assignment_date
            })
        type_name = CurriculumType.objects.get(id=type_id).name
        context = {
            "subject_id": subject_id, "type_id": type_id, "curriculum_id": curriculum_id, "type_name": type_name,
            "object": curriculum_object, "objects": student_objects
        }
        return context

    # 공지사항
    if type_id == 1:
        if method == "detail":
            type_name = CurriculumType.objects.get(id=type_id).name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object
            }
        elif method == "create":
            context = {
                "subject_id": subject_id, "type_id": type_id
            }
        elif method == "modify":
            context = {
                "subject_id": subject_id, "type_id": type_id, "object": curriculum_object, "method": method
            }
    # 지침서
    elif type_id == 2:
        if method == "create":
            context = {
                "subject_id": subject_id, "type_id": type_id
            }
        elif method == "modify":
            context = {
                "subject_id": subject_id, "type_id": type_id, "object": curriculum_object, "method": method
            }
    elif type_id == 3:
        if method == "create":
            checklist_objects = ChecklistSet.objects.all()
            context = {
                "subject_id": subject_id, "type_id": type_id,
                "checklist_objects": checklist_objects, "method": method
            }
        elif method == "modify":
            checklist_objects = ChecklistSet.objects.all()
            checklist_set = ChecklistCurriculum.objects.get(curriculum_id=curriculum_id).checklist_set
            selected_checklist_objects = ChecklistGroup.objects.filter(set=checklist_set).all()
            evaluation_status = Evaluation.objects.get(curriculum=curriculum_object).status
            context = {
                "subject_id": subject_id, "type_id": type_id, "object": curriculum_object, "method": method,
                "selected_checklist_objects": selected_checklist_objects, "checklist_objects": checklist_objects,
                "checklist_set_id": checklist_set.id, "evaluation_status": evaluation_status
            }
    elif type_id == 4:
        if method == "create":
            context = {
                "subject_id": subject_id, "type_id": type_id
            }
        elif method == "modify":
            evaluation_status = Evaluation.objects.get(curriculum=curriculum_object).status
            context = {
                "subject_id": subject_id, "type_id": type_id, "object": curriculum_object, "method": method,
                "evaluation_status": evaluation_status
            }
    elif type_id == 5:
        if method == "create":
            context = {
                "subject_id": subject_id, "type_id": type_id
            }
        elif method == "modify":
            evaluation_status = Evaluation.objects.get(curriculum=curriculum_object).status
            context = {
                "subject_id": subject_id, "type_id": type_id, "object": curriculum_object, "method": method,
                "evaluation_status": evaluation_status
            }
    return context


def assignment_context(request, subject_id, curriculum_id, type_id, assignment_id):
    curriculum_object = Curriculum.objects.get(id=curriculum_id)
    assignment_object = Assignment.objects.get(id=assignment_id)
    type_name = curriculum_object.type.name
    context = {
        "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
        "object": curriculum_object, "assignment_object": assignment_object
    }

    if type_id == 3:
        checklist_objects = []
        checklist_set_object = ChecklistCurriculum.objects.get(curriculum=curriculum_object).checklist_set
        checklist_group_object = ChecklistGroup.objects.filter(set=checklist_set_object)
        for i in checklist_group_object:
            checklist_record = ChecklistRecord.objects.filter(checklist=i, assignment=assignment_object,
                                                              author__profile__group__name="student")
            if checklist_record.exists():
                record = checklist_record.get().record
            else:
                record = None
            checklist_objects.append({
                "id": i.id,
                "content": i.checklist.content,
                "record": record
            })
        context["checklist_objects"] = checklist_objects

    return context


def evaluation_context(request, subject_id, curriculum_id, type_id, assignment_id):
    checklist_objects = []
    checklist_set_object = ChecklistCurriculum.objects.get(curriculum_id=curriculum_id).checklist_set
    checklist_group_object = ChecklistGroup.objects.filter(set=checklist_set_object)
    for i in checklist_group_object:
        checklist_record = ChecklistRecord.objects.filter(checklist=i, assignment_id=assignment_id,
                                                          author__profile__group__name="professor")
        if checklist_record.exists():
            record = checklist_record.get().record
        else:
            record = None
        checklist_objects.append({
            "id": i.id,
            "content": i.checklist.content,
            "record": record
        })
    context = {"subject_id": subject_id, "type_id": type_id, "curriculum_id": curriculum_id,
               "assignment_id": assignment_id, "checklist_objects": checklist_objects}
    return context
