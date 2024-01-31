from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
                  path("", include("common.urls")),
                  path("p/", include("professor.urls")),
                  path("s/", include("student.urls")),
                  path("api/", include("api.urls")),
                  path("admin/", include("admin.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
