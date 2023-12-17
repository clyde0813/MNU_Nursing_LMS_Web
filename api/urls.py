from django.urls import path, include
from api import views

app_name = 'api'

urlpatterns = [
    path("<int:assignment_id>/comment", views.comment_web, name="comment_web"),
    path("<int:type_id>/checklist", views.checklist_api)
]
