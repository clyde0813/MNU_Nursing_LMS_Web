from models.models import *


def assignment_create(request, subject_id, type_id, curriculum_id):
    title = request.POST.get("title")
    content = request.POST.get("content")
    assignment = Assignment.objects.create(title=title, content=content, curriculum_id=curriculum_id,
                                           author=request.user)
    if type_id == 3:
        checklist_set_object = ChecklistCurriculum.objects.get(curriculum_id=curriculum_id).checklist_set
        checklist_group = ChecklistGroup.objects.filter(set=checklist_set_object)
        for i in checklist_group:
            checklist_record = request.POST.get("check_" + str(i.id))
            if checklist_record is not None:
                ChecklistRecord.objects.create(assignment=assignment, author=request.user, checklist=i,
                                               record=int(checklist_record))
    elif type_id == 5:
        print(request.POST.get("date"))
        AssignmentPeriod.objects.create(assignment=assignment, date=request.POST.get("date"))


def curriculum_context(request, subject_id, curriculum_id, type_id, method):
    curriculum_object = Curriculum.objects.get(id=curriculum_id)
    context = None

    if type_id != 1 and method == "detail":
        assignment_object = Assignment.objects.get(curriculum_id=curriculum_id, author=request.user)
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
                checklist_record = ChecklistRecord.objects.filter(author=request.user, checklist=i,
                                                                  assignment=assignment_object)
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

    if type_id == 1:
        type_name = curriculum_object.type.name
        context = {
            "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
            "object": curriculum_object
        }
    elif type_id in [2, 4, 5]:
        if method == "create":
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object
            }
    elif type_id == 3:
        if method == "create":
            checklist_set_object = ChecklistCurriculum.objects.get(curriculum=curriculum_object).checklist_set
            checklist_objects = ChecklistGroup.objects.filter(set=checklist_set_object)
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object, "checklist_objects": checklist_objects
            }
    return context
