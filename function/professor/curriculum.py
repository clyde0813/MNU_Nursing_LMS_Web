from models.models import *


def curriculum_context(subject_id, type_id, curriculum_id, method):
    curriculum_object = None
    subject_name = Subject.objects.get(id=subject_id).name

    if curriculum_id is not None:
        curriculum_object = Post.objects.get(id=curriculum_id)
        file_objects = PostFile.objects.filter(post_id=curriculum_id).all()
    if type_id != 1 and method == "detail":
        student_objects = []
        for obj in Enrollment.objects.filter(subject_id=subject_id):
            assignment_object = Post.objects.filter(child_post__parent_post_id=curriculum_id, author=obj.student)
            if assignment_object.exists():
                assignment_id = assignment_object.get().id
                assignment_date = assignment_object.get().created_date
                if PostDeadline.objects.filter(post=curriculum_object).exists() and \
                        PostDeadline.objects.get(post=curriculum_object).deadline.date() <= assignment_date.date():
                    assignment_status = 2
                else:
                    assignment_status = True
            else:
                assignment_id = None
                assignment_date = None
                assignment_status = False
            student_objects.append({
                "id": assignment_id,
                "student": obj.student,
                "assignment_date": assignment_date,
                "assignment_status": assignment_status
            })
        type_name = PostType.objects.get(id=type_id).name
        context = {
            "subject_id": subject_id, "type_id": type_id, "curriculum_id": curriculum_id, "subject_name": subject_name,
            "type_name": type_name, "object": curriculum_object, "objects": student_objects, "files": file_objects
        }
        return context

    context = {
        "subject_id": subject_id,
        "type_id": type_id,
        "subject_name": subject_name,
        "type_name": PostType.objects.get(id=type_id).name,
        "files": PostFile.objects.filter(post=curriculum_object).all(),
        "input_list": {
            "title": True,
            "content": True,
            "deadline": False,
            "evaluation": False,
            "checklist": False,
            "period": False
        }
    }

    # 공지사항
    if type_id == 1:
        if method == "detail":
            context.update({
                "object": curriculum_object
            })
        elif method == "modify":
            context.update({
                "object": curriculum_object,
                "method": method
            })
    # 지침서
    elif type_id == 2:
        if method == "create":
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
            }
        elif method == "modify":
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
                "object": curriculum_object,
                "method": method
            }
    # 핵심수기술
    elif type_id == 3:
        if method == "create":
            checklist_objects = ChecklistSet.objects.all()
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
                "checklist_objects": checklist_objects,
                "method": method
            }
        elif method == "modify":
            checklist_objects = ChecklistSet.objects.all()
            checklist_set = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
            selected_checklist_objects = ChecklistGroup.objects.filter(set=checklist_set).all()
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
                "object": curriculum_object,
                "method": method,
                "selected_checklist_objects": selected_checklist_objects,
                "checklist_objects": checklist_objects,
                "checklist_set_id": checklist_set.id,
            }
    # 과제
    elif type_id == 4:
        if method == "create":
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
            }
        elif method == "modify":
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
                "object": curriculum_object,
                "method": method
            }
    # 실습일지
    elif type_id == 5:
        if method == "create":
            context["input_list"]["period"] = True
        elif method == "modify":
            context = {
                "subject_id": subject_id,
                "type_id": type_id,
                "subject_name": subject_name,
                "object": curriculum_object,
                "method": method
            }
    return context


def assignment_context(request, subject_id, curriculum_id, type_id, assignment_id):
    curriculum_object = Post.objects.get(id=curriculum_id)
    assignment_object = Post.objects.get(id=assignment_id)
    file_objects = PostFile.objects.filter(post_id=curriculum_id).all()
    type_name = curriculum_object.type.name
    score_status = PostEvaluationStatus.objects.filter(post=curriculum_object)
    score = None
    if score_status.exists() and score_status.get().status:
        if PostEvaluation.objects.filter(post_id=curriculum_id).exists():
            score = PostEvaluation.objects.filter(post_id=curriculum_id).get().percentage
        else:
            score = 0
    print(score)

    context = {
        "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
        "object": curriculum_object, "assignment_object": assignment_object, "video": None,
        "files": file_objects, "score": score
    }

    if type_id == 3:
        checklist_objects = []
        checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
        checklist_group_object = ChecklistGroup.objects.filter(set=checklist_set_object)
        for i in checklist_group_object:
            checklist_record = ChecklistRecord.objects.filter(
                checklist=i,
                author=assignment_object.author,
                target=assignment_object.author,
                post_id=curriculum_id,
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
        if PostFile.objects.filter(post=assignment_object, file_extension="video").exists():
            context["video"] = PostFile.objects.filter(post=assignment_object, file_extension="video").get()
        context["checklist_objects"] = checklist_objects

    return context
