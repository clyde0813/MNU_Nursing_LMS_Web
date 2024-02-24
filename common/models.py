from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    userID = models.IntegerField(null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=300)
