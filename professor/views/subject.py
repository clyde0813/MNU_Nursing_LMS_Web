from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


@login_required(redirect_field_name=None)
def subject_create(request):
    name = request.POST.get("name")
    subject_object = Subject.objects.create(professor=request.user, name=name)
    for i in range(2, 6):
        SubjectEvaluationItem.objects.create(
            subject=subject_object,
            post_type_id=i,
            name=PostType.objects.get(id=i).name,
            percentage=25
        )
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
