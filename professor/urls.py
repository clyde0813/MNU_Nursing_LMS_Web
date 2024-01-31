from django.urls import path
from professor import views

app_name = "professor"

urlpatterns = [
    path("subject/add", views.subject_create, name="subject_create"),
    path("subject/delete/<int:subject_id>", views.subject_delete, name="subject_delete"),
    path("subject/modify", views.subject_modify, name="subject_modify"),

    path("<int:subject_id>/<int:type_id>", views.curriculum, name="curriculum"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>", views.curriculum_detail, name="curriculum_detail"),
    path("<int:subject_id>/<int:type_id>/create", views.curriculum_create, name="curriculum_create"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>/modify", views.curriculum_modify,
         name="curriculum_modify"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>/delete", views.curriculum_delete,
         name="curriculum_delete"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>/<int:assignment_id>", views.assignment_detail,
         name="assignment_detail"),
    path("<int:subject_id>/<int:type_id>/<int:curriculum_id>/<int:student_id>/evaluate", views.assignment_evaluate,
         name="assignment_evaluate"),

    # 교수 일지
    path("<int:subject_id>/journal", views.journal, name="journal"),
    path("<int:subject_id>/journal/<int:journal_id>", views.journal_detail, name="journal_detail"),
    path("<int:subject_id>/journal/create", views.journal_create, name="journal_create"),

    # 학생 평가
    path("<int:subject_id>/student/evaluate", views.student_evaluate, name="student_evaluate"),

    # 교수 평가
    path("<int:subject_id>/professor/evaluate", views.professor_evaluate, name="professor_evaluate"),
    path("<int:subject_id>/professor/evaluate/<int:student_id>", views.professor_evaluate_detail,
         name="professor_evaluate_detail"),

    path("<int:subject_id>/enroll", views.enrollment, name="enrollment"),
    path("<int:subject_id>/enroll/<int:enrollment_id>", views.enrollment_confirm, name="enrollment_confirm"),
]
