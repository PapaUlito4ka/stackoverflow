from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.hashers import check_password, make_password
import datetime
from django.utils.timezone import now
import json


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    img_path = models.CharField(default='anonymous.jpg', max_length=64)
    location = models.CharField(default='', max_length=64)
    title = models.CharField(default='', max_length=64)
    about = models.TextField(default='')

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def check_user(username, password):
        try:
            user = User.objects.get(username=username)
        except:
            return False
        if password == user.password:
            return True
        return False

    def __setattr__(self, name, value):
        if name != 'password':
            return super().__setattr__(name, value)
        self.salt = 12
        self.plainPassword = value
        return super().__setattr__(name, make_password(value))

    def __getattribute__(self, name):
        if name != 'password':
            return super().__getattribute__(name)
        return self.plainPassword


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    count = models.IntegerField(default=1)


class Question(models.Model):
    title = models.CharField(max_length=128)
    votes = models.IntegerField(default=0) 
    views = models.IntegerField(default=0)
    text = models.TextField()

    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Answer(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)

