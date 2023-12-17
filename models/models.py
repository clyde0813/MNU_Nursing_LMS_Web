from django.db import models
from django.contrib.auth.models import User
from sqlparse.sql import Assignment


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class CurriculumType(models.Model):
    name = models.CharField(max_length=100)


class Curriculum(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    type = models.ForeignKey(CurriculumType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)


class Period(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    date = models.DateField()


class Checklist(models.Model):
    content = models.CharField(max_length=1000)


class ChecklistSet(models.Model):
    name = models.CharField(max_length=100)


class ChecklistGroup(models.Model):
    set = models.ForeignKey(ChecklistSet, on_delete=models.CASCADE)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)


class ChecklistCurriculum(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    checklist_set = models.ForeignKey(ChecklistSet, on_delete=models.CASCADE)


class Assignment(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class AssignmentPeriod(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    date = models.DateField()


class ChecklistRecord(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.IntegerField()
    checklist = models.ForeignKey(ChecklistGroup, on_delete=models.CASCADE)


class Comment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
