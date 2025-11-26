from django.db import models
from user.models import User  # users 앱의 User 모델 임포트
# courses 앱에서 참조할 모델 임포트
from courses.models import Class, ClassComment


# 메신저 채널
class MessengerChannel(models.Model):
    channel_name = models.CharField(max_length=100, verbose_name="채널명")

    channel_type_choices = (
        ('counslation', '상담'),
        ('coordination', '조율'),
    )

    channel_type = models.CharField(max_length=20, verbose_name="채널 유형")  # 상담, 조율 등 태그
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'messenger_channel'
        verbose_name = '메신저 채널'
        verbose_name_plural = '메신저 채널 목록'

    def __str__(self):
        return self.channel_name if self.channel_name else f"Channel {self.id}"

# 채널 참여자
class ChannelMember(models.Model):
    channel = models.ForeignKey(MessengerChannel, on_delete=models.CASCADE, verbose_name="채널")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")

    class Meta:
        db_table = 'channel_member'
        verbose_name = '채널 멤버'
        verbose_name_plural = '채널 멤버 목록'
        unique_together = ('channel', 'user')  # 복합 기본 키 역할

    def __str__(self):
        return f"{self.channel.channel_name} - {self.user.name}"


# 메신저 메시지
class MessengerMessage(models.Model):
    channel = models.ForeignKey(MessengerChannel, on_delete=models.CASCADE, verbose_name="채널")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="보낸 사람")
    content = models.TextField(verbose_name="내용")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="전송 일시")
    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")

    class Meta:
        db_table = 'messenger_messages'
        verbose_name = '메신저 메시지'
        verbose_name_plural = '메신저 메시지 목록'

    def __str__(self):
        return f"{self.sender.name}: {self.content[:20]}..."