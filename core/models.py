from django.db import models
from user.models import User  # user 앱의 User 모델 임포트
# courses 앱에서 참조할 모델 임포트
from courses.models import Class, ClassComment

# 캘린더 이벤트
class CalendarEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="강의")
    title = models.CharField(max_length=100, verbose_name="제목")
    description = models.TextField(verbose_name="설명")
    start_time = models.DateTimeField(verbose_name="시작 시간")
    end_time = models.DateTimeField(verbose_name="종료 시간")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")

    class Meta:
        db_table = 'calendar_event'
        verbose_name = '캘린더 이벤트'
        verbose_name_plural = '캘린더 이벤트 목록'

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

# 알림
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="수신 사용자")
    notification_type = models.CharField(max_length=30, verbose_name="알림 유형")
    message = models.TextField(verbose_name="메시지")
    event = models.ForeignKey(CalendarEvent, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="이벤트 참조")
    class_comment = models.ForeignKey(ClassComment, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="강의 댓글 참조")
    community_comment = models.ForeignKey(CommunityComment, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name="커뮤니티 댓글 참조")

    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'notification'
        verbose_name = '알림'
        verbose_name_plural = '알림 목록'

    def __str__(self):
        return f"[{self.notification_type}] {self.message[:30]}..."