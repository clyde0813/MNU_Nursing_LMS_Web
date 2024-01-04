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