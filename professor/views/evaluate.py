from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


@login_required(redirect_field_name=None)
def student_evaluate(request, subject_id):
    context = {"subject_id": subject_id, "type_id": 7}
    return render(request, "professor/student_evaluation/evaluation_list.html", context)


@login_required(redirect_field_name=None)
def professor_evaluate(request, subject_id):
    student_objects = User.objects.filter(profile__group__name="student", enrollment__subject_id=subject_id,
                                          enrollment__status=True).all()
    evaluation_objects = Evaluation.objects.filter(curriculum__subject_id=subject_id).all().order_by(
        "curriculum__type_id")
    context = {"subject_id": subject_id, "student_objects": student_objects,
               "evaluation_objects": evaluation_objects, "type_id": 8}
    return render(request, "professor/professor_evaluation/evaluation_list.html", context)
