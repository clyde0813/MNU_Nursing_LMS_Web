from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from common.models import Group, Profile
import professor.views
import student.views


# Create your views here.
def index(request):
    # 로그인 Post
    if request.method == "POST":
        username = request.POST.get("username", default=None)
        password = request.POST.get("password", default=None)
        # 인증
        user = authenticate(request, username=username, password=password)
        # 인증 실패
        if user is None:
            context = {"error": "로그인 정보가 정확하지 않습니다."}
            return render(request, "common/login/login.html", context)
        # 인증 성공
        if user.profile.group.name == "professor":
            login(request, user)
            return professor.views.index(request)
        if user.profile.group.name == "student":
            login(request, user)
            return student.views.index(request)
    # 로그인 Get
    else:
        # 이미 로그인 한 경우
        if request.user.is_authenticated:
            if request.user.profile.group.name == "professor":
                return professor.views.index(request)
            if request.user.profile.group.name == "student":
                return student.views.index(request)
        # 로그인 하지 않은 경우
        else:
            return render(request, "common/login/login.html")


def logout(request):
    auth.logout(request)
    return redirect("common:index")


def register(request, roleName):
    # 가입 POST
    if request.method == "POST":
        if roleName == "professor":
            group = Group.objects.get(name="professor")
            userID = None
        elif roleName == "student":
            group = Group.objects.get(name="student")
            userID = request.POST.get("studentID", default=None)
        else:
            return redirect("common:index")

        name = request.POST.get("name", default=None)
        username = request.POST.get("username", default=None)
        password = request.POST.get("password", default=None)
        password2 = request.POST.get("password2", default=None)
        if password != password2:
            return 0
        mobile = request.POST.get("mobile", default=None)
        email = request.POST.get("email", default=None)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, name=name, mobile=mobile, userID=userID, university_id=1, group=group)

        user_auth = authenticate(request, username=username, password=password)
        login(request, user_auth)
        return redirect("common:index")

    # 가입 GET
    else:
        if roleName == "professor":
            return render(request, "common/register/professor_register.html")
        elif roleName == "student":
            return render(request, "common/register/student_register.html")
        else:
            return redirect("common:index")


def profile(request):
    if request.method == "POST":
        password = request.POST.get("password", default=None)
        mobile = request.POST.get("mobile", default=None)
        email = request.POST.get("email", default=None)
        user_object = User.objects.get(id=request.user.id)
        profile_object = Profile.objects.get(user_id=request.user.id)
        if password is not None and len(password) > 8:
            user_object.set_password(password)
        if email is not None:
            user_object.email = email
        profile_object.mobile = mobile
        user_object.save()
        profile_object.save()
        return redirect("common:profile")
    profile_object = Profile.objects.get(user=request.user)
    context = {"profile_object": profile_object}
    return render(request, "professor/layout/profile.html", context)
