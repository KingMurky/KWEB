from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10)
    studentId = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)


class Lecture(models.Model):
    lecturename = models.CharField(max_length=100)
    professor = models.CharField(max_length=50)
    year = models.CharField(max_length=10, null=True)
    semester = models.CharField(max_length=10, null=True)


class LecturePost(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lecture_id')
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Takes(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lecture_id')
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='user_id')
