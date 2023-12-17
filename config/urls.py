from django.urls import path, include

urlpatterns = [
    path("", include("common.urls")),
    path("p/", include("professor.urls")),
    path("s/", include("student.urls")),
    path("api/", include("api.urls"))
]
