from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


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
