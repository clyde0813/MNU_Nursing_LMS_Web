from django.urls import path, include
from api import views

app_name = 'api'

urlpatterns = [
    path("login", views.login),
    path("student", views.student),
    path("student/progress", views.progress),
    path("subject/list", views.subject),
    path("curriculum", views.curriculum),
    path("comment", views.comment),
    path("<int:assignment_id>/comment", views.comment_web, name="comment_web"),
    path("<int:type_id>/checklist", views.checklist_api),
    path("pdf", views.pdfViewer, name="pdfViewer")
]
