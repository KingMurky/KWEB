from django.contrib import admin
from .models import Account, Takes, Lecture, LecturePost
# Register your models here.

admin.site.register(Account)
admin.site.register(Lecture)
admin.site.register(LecturePost)
admin.site.register(Takes)
