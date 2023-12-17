from django.urls import path
from student import views

app_name = "student"
urlpatterns = [
    path("enrollment/<int:subject_id>", views.enrollment, name="enrollment"),
    path("<int:subject_id>/<int:type_id>", views.curriculum, name="curriculum"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>", views.curriculum_detail, name="curriculum_detail"),
]
