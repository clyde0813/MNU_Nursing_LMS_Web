from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


@login_required(redirect_field_name=None)
# Create your views here.
def index(request):
    subject_objects = Subject.objects.filter(professor=request.user).all()
    context = {"subject_objects": subject_objects}
    return render(request, "professor/subject/list.html", context)


@login_required(redirect_field_name=None)
def subject_create(request):
    name = request.POST.get("name")
    Subject.objects.create(professor=request.user, name=name)
    return redirect("common:index")


@login_required(redirect_field_name=None)
def subject_delete(request, subject_id):
    Subject.objects.get(professor=request.user, id=subject_id).delete()
    return redirect("common:index")


@login_required(redirect_field_name=None)
def subject_modify(request):
    subject_id = request.POST.get("subject_id")
    subject_object = Subject.objects.get(professor=request.user, id=int(subject_id))
    subject_object.name = request.POST.get("name")
    subject_object.save()
    return redirect("common:index")


@login_required(redirect_field_name=None)
def curriculum(request, subject_id, type_id):
    curriculum_objects = Curriculum.objects.filter(subject_id=subject_id, type_id=type_id) \
        .order_by("created_date").all()
    type_name = CurriculumType.objects.get(id=type_id).name
    subject_name = Subject.objects.get(id=subject_id).name
    context = {"subject_id": subject_id, "type_id": type_id, "subject_name": subject_name, "type_name": type_name,
               "objects": curriculum_objects}
    return render(request, "professor/list/list_layout.html", context)


@login_required(redirect_field_name=None)
def curriculum_create(request, subject_id, type_id):
    if request.method == "POST":
        curriculum_create_func(request, subject_id, type_id)
        return redirect("professor:curriculum", subject_id, type_id)
    context = curriculum_context(subject_id, type_id, None, "create")
    return render(request, html_return(type_id, "create"), context)


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


def journal(request, subject_id):
    context = {"subject_id": subject_id, "type_id": 6}
    return render(request, "professor/journal/journal_list.html", context)


def journal_create(request, subject_id):
    student_objects = Enrollment.objects.filter(subject_id=subject_id, status=True)

    context = {"subject_id": subject_id, "student_objects": student_objects, "type_id": 6}
    return render(request, "professor/journal/journal_create.html", context)


@login_required(redirect_field_name=None)
def enrollment(request, subject_id):
    subject_name = Subject.objects.get(id=subject_id).name
    enrollment_objects = Enrollment.objects.filter(subject_id=subject_id).all()
    context = {"subject_id": subject_id, "side_nav": "enrollment", "subject_name": subject_name,
               "enrollment_objects": enrollment_objects}
    return render(request, "professor/subject/enrollment.html", context)


@login_required(redirect_field_name=None)
def enrollment_confirm(request, subject_id, enrollment_id):
    enrollment_object = Enrollment.objects.get(id=enrollment_id)
    enrollment_object.status = True
    enrollment_object.save()
    return redirect("professor:enrollment", subject_id)
