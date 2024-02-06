import datetime

from django.db import models
from django.contrib.auth.models import User
from sqlparse.sql import Assignment
import time
import string
import random


# 파일 업로드 경로 보안
def dynamic_upload_to(self, filename):
    _LENGTH = 10  # 10자리
    string_pool = string.ascii_lowercase  # 소문자
    result = ""  # 결과 값
    for i in range(_LENGTH):
        result += random.choice(string_pool)  # 랜덤한 문자열 하나 선택
    date = datetime.datetime.now().strftime("%Y%m%d")
    return f"{date}/{result}/{filename}"


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(default=None, null=True)
    status = models.BooleanField(default=False)


class PostType(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(PostType, on_delete=models.CASCADE)


class PostSubjectMapping(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostPostMapping(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="parent_post")
    child_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="child_post")


class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to=dynamic_upload_to)
    filename = models.CharField(max_length=100)
    file_extension = models.CharField(max_length=100, null=True)


class PostPeriod(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)


class PostDeadline(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deadline = models.DateTimeField()


class PostLocation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)


class PostUserMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class SubjectEvaluationItem(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE, blank=True, null=True)
    percentage = models.IntegerField(default=0)


class PostEvaluationStatus(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class PostEvaluation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True)
    target = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    percentage = models.IntegerField(default=0)


# class Curriculum(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     type = models.ForeignKey(CurriculumType, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     eval_status = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#
# class CurriculumFile(models.Model):
#     curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=dynamic_upload_to)
#     filename = models.CharField(max_length=100)


# class Period(models.Model):
#     curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
#     date = models.DateField()


class Checklist(models.Model):
    sequence = models.IntegerField()
    content = models.CharField(max_length=1000)
    essential = models.BooleanField(default=False)
    type = models.CharField(max_length=100, default="hand")


class ChecklistSet(models.Model):
    name = models.CharField(max_length=100)


class ChecklistGroup(models.Model):
    set = models.ForeignKey(ChecklistSet, on_delete=models.CASCADE)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)


class PostChecklistMapping(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    checklist_set = models.ForeignKey(ChecklistSet, on_delete=models.CASCADE)


# class Evaluation(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     percentage = models.IntegerField(default=0)

# class Assignment(models.Model):
#     curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True)


# class AssignmentFile(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=dynamic_upload_to)
#     filename = models.CharField(max_length=100)


# class AssignmentVideo(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=dynamic_upload_to)
#     filename = models.CharField(max_length=100)


# class AssignmentPeriod(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     date = models.DateField()


# class Journal(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_date = models.DateTimeField()
#     location = models.CharField(max_length=100, default=None, null=True)


# class JournalStudent(models.Model):
#     journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
#     student = models.ForeignKey(User, on_delete=models.CASCADE)


class ChecklistRecord(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checklist_author")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checklist_target")
    record = models.IntegerField()
    checklist = models.ForeignKey(ChecklistGroup, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
