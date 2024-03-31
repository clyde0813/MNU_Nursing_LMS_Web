from django.urls import path, include
from common import views

app_name = "common"
urlpatterns = [
    path("", views.index, name="index"),
    path("/logout", views.logout, name="logout"),
    path("/register/<str:roleName>", views.register, name="register"),
    path("/profile", views.profile,  name="profile"),

]
