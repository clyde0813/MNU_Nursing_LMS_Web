from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4

from models.models import *
from common.models import *


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"error": "User not found"}, status=403)
        else:
            token = Token.objects.filter(user=user)
            group = user.profile.group.name
            return_token = ""
            if token.exists():
                return_token = token.get().token
            else:
                token = Token.objects.create(user=user, token=uuid4())
                return_token = token.token
            return JsonResponse({"token": return_token, "group": group}, status=200)


def progress(request):
    return_json = {"progress": []}
    token = request.headers.get('Token')
    user = Token.objects.filter(token=token).get().user
    subjects = Enrollment.objects.filter(student=user).all()
    for data in subjects:
        curriculum_count = Post.objects.filter(type_id__in=[2, 3, 4, 5],
                                               postsubjectmapping__subject=data.subject).all().count()
        assignment_count = Post.objects.filter(type_id=7,
                                               child_post__parent_post__postsubjectmapping__subject=data.subject).all().count()
        progress = round((assignment_count / curriculum_count) * 100) if assignment_count != 0 else 0
        return_json["progress"].append({"name": data.subject.name, "progress": progress})
    return JsonResponse(return_json, status=200)


def subject(request):
    return_json = {"subject": []}
    token = request.headers.get('Token')
    user = Token.objects.filter(token=token).get().user
    if user.profile.group.name == "professor":
        subjects = Subject.objects.filter(professor=user).all()
        for data in subjects:
            return_json["subject"].append({"id": data.id, "name": data.name, "professor": user.profile.name})
    else:
        subjects = Enrollment.objects.filter(student=user).all()
        for data in subjects:
            return_json["subject"].append(
                {"id": data.subject.id, "name": data.subject.name, "professor": data.subject.professor.profile.name})
    return JsonResponse(return_json, status=200)


def curriculum(request):
    return_json = {"curriculum": []}
    token = request.headers.get('Token')
    subject_id = request.GET.get('subject')
    user = Token.objects.filter(token=token).get().user
    curriculums = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id__in=[2, 3, 4, 5]).all()
    for data in curriculums:
        assignment_id = 0
        if user.profile.group.name == "student":
            assignment = Post.objects.filter(child_post__parent_post=data, author=user, type_id=7)
            if assignment.exists():
                assignment_id = assignment.get().id
        return_json["curriculum"].append(
            {"id": data.id, "name": data.title, "content": data.content, "type": data.type.name,
             "assignment": assignment_id})
    return JsonResponse(return_json, status=200)


def student(request):
    return_json = {"student": []}
    token = request.headers.get('Token')
    subject_id = request.GET.get('subject')
    curriculum_id = request.GET.get('curriculum')
    user = Token.objects.filter(token=token).get().user
    students = User.objects.filter(enrollment__subject_id=subject_id).all()
    for data in students:
        id = None
        status = False
        assignment = Post.objects.filter(author=data, type_id=7, child_post__parent_post_id=curriculum_id)
        if assignment.exists():
            id = assignment.get().id
            status = True
        return_json["student"].append({"assignment": id, "name": data.profile.name, "status": status})
    return JsonResponse(return_json, status=200)


@csrf_exempt
def comment(request):
    if request.method == "POST":
        print("!!")
        token = request.headers.get('Token')
        assignment_id = request.POST.get('assignment')
        content = request.POST.get('comment')
        user = Token.objects.filter(token=token).get().user
        Comment.objects.create(author=user, content=content, post_id=assignment_id)
        return JsonResponse({"status": 200}, status=200)

    return_json = {"comment": []}
    token = request.headers.get('Token')
    assignment = request.GET.get('assignment')
    print(assignment)
    comments = Comment.objects.filter(post_id=assignment).all()
    for data in comments:
        author = ""
        date = str(data.created_date.strftime("%Y-%m-%d"))
        if data.author.profile.group.name == "professor":
            author = data.author.profile.name + " 교수님"
        else:
            author = data.author.profile.name + " 학생"
        return_json["comment"].append({"content": data.content, "author": author, "date": date})
    print(return_json)
    return JsonResponse(return_json, status=200)


def comment_web(request, assignment_id):
    if request.method == "POST":
        content = request.POST["content"]
        Comment.objects.create(content=content, post_id=assignment_id, author=request.user)
    return redirect(request.META.get('HTTP_REFERER'))


def checklist_api(request, type_id):
    if type_id == 3:
        checklist_set_id = request.GET.get("checklist_set_id")
        checklist_objects = ChecklistGroup.objects.filter(set_id=checklist_set_id).all()
        print(checklist_set_id, checklist_objects)
        return_json = []
        for i in checklist_objects:
            return_json.append({
                "id": i.id,
                "content": i.checklist.content
            })
    return JsonResponse(return_json, safe=False)


def pdfViewer(request):
    file = request.GET.get("file", None)
    context = {"file": file}
    return render(request, "common/layout/pdf.html", context)
