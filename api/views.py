from django.http import JsonResponse
from django.shortcuts import render, redirect
from models.models import Checklist, ChecklistSet, ChecklistGroup, Comment


# Create your views here.
def comment_web(request, assignment_id):
    if request.method == "POST":
        content = request.POST["content"]
        Comment.objects.create(content=content, assignment_id=assignment_id, author=request.user)
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
