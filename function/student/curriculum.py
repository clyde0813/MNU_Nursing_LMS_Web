from models.models import *


def curriculum_context(request, subject_id, curriculum_id, type_id, method):
    curriculum_object = Post.objects.get(id=curriculum_id)
    context = None

    if type_id != 1 and method == "detail":
        assignment_object = Post.objects.get(child_post__parent_post_id=curriculum_id, author=request.user)
        type_name = curriculum_object.type.name
        context = {
            "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
            "object": curriculum_object, "assignment_object": assignment_object,
            "files": curriculum_object.postfile_set.all(), "video": None
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

        return context

    if type_id == 1:
        type_name = curriculum_object.type.name
        context = {
            "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
            "object": curriculum_object, "files": curriculum_object.postfile_set.all()
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
            checklist_set_object = PostChecklistMapping.objects.get(post_id=curriculum_id).checklist_set
            checklist_objects = ChecklistGroup.objects.filter(set=checklist_set_object)
            type_name = curriculum_object.type.name
            context = {
                "subject_id": subject_id, "type_id": type_id, "type_name": type_name,
                "object": curriculum_object, "checklist_objects": checklist_objects
            }
    return context
