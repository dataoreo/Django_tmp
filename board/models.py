

# Create your models here.

# board/models.py

from django.db import models
from user.models import User


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    views = models.IntegerField(default=0, verbose_name="조회수")
    is_pinned = models.BooleanField(default=False, verbose_name="상단 고정")

    class Meta:
        db_table = 'notice'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 목록'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

