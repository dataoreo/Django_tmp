

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

# 커뮤니티 게시판
class CommunityBoard(models.Model):
    board_id = models.AutoField(primary_key=True)
    board_title = models.CharField(max_length=100, verbose_name="게시판 제목")
    board_type = models.CharField(max_length=20, verbose_name="게시판 유형")

    class Meta:
        db_table = 'community_board'
        verbose_name = '커뮤니티 게시판'
        verbose_name_plural = '커뮤니티 게시판 목록'

    def __str__(self):
        return self.board_title

# 커뮤니티 게시글
class CommunityPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    board = models.ForeignKey(CommunityBoard, on_delete=models.CASCADE, verbose_name="게시판")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    post_title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")
    open = models.BooleanField(default=True, verbose_name="공개 여부")
    view = models.IntegerField(default=0, verbose_name="조회수")

    class Meta:
        db_table = 'community_post'
        verbose_name = '커뮤니티 게시글'
        verbose_name_plural = '커뮤니티 게시글 목록'

    def __str__(self):
        return self.post_title

# 커뮤니티 댓글
class CommunityComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, verbose_name="게시글")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    comment_content = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'community_comment'
        verbose_name = '커뮤니티 댓글'
        verbose_name_plural = '커뮤니티 댓글 목록'

    def __str__(self):
        return f"{self.author.name}의 댓글 ({self.post.post_title})"