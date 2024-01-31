from django.urls import path, include
from admin import views

app_name = "admin"
urlpatterns = [
    path("checklist/update", views.checklistUpdate, name="checklist-update")
]
