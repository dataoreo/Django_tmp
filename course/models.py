# course/models.py

from django.db import models
from user.models import User


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="강사")
    title = models.CharField(max_length=200, verbose_name="강의명")
    description = models.TextField(verbose_name="강의 설명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    views = models.IntegerField(default=0, verbose_name="조회수")
    is_active = models.BooleanField(default=True, verbose_name="활성화")

    class Meta:
        db_table = 'course'
        verbose_name = '강의'
        verbose_name_plural = '강의 목록'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
