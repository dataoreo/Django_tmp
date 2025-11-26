from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# 역할 자동 부여를 위한 인증 코드
instructor_code = "ISNTRUCTOR_00"
manager_code = "MANAGER_01"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=30, verbose_name="이름", null=False, blank=False)
    email = models.EmailField(max_length=50, verbose_name="아이디(이메일)", unique=True, null=False, blank=False)
    role_choices = (('student', '학생'), ('instructor', '강사'), ('manager', '매니저'))
    role = models.CharField(max_length=10, choices=role_choices, default='student', verbose_name='역할')
    phone_number = models.CharField(max_length=15, verbose_name="전화번호", unique=True,
                                   default='010-0000-0000', null=False, blank=True)
    address = models.CharField(max_length=100, verbose_name="주소", null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="생년월일")
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="프로필 사진")
    code = models.CharField(max_length=15, verbose_name="기관 인증코드", null=True, blank=True)

    # 👇 [추가] 이메일 인증 관련 필드
    email_verified = models.BooleanField(default=False, verbose_name="이메일 인증 여부")
    email_verification_token = models.UUIDField(default=uuid.uuid4, verbose_name="이메일 인증 토큰")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None and self.code:
            if self.code == instructor_code:
                self.role = "instructor"
            elif self.code == manager_code:
                self.role = "manager"
        super().save(*args, **kwargs)

    def is_student(self):
        return self.role == 'student' or self.role == '학생'

    def is_instructor(self):
        return self.role == 'instructor' or self.role == '강사'

    def is_manager(self):
        return self.role == 'manager' or self.role == '매니저'


class DIMC(models.Model):
    test_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT)  # User 모델 참조
    pdf_path = models.TextField(verbose_name="PDF 파일 경로")
    D_score = models.IntegerField(verbose_name="D 점수")
    I_score = models.IntegerField(verbose_name="I 점수")
    M_score = models.IntegerField(verbose_name="M 점수")
    C_score = models.IntegerField(verbose_name="C 점수")
    result = models.TextField(verbose_name="테스트 결과")
    tested_at = models.DateTimeField(auto_now_add=True, verbose_name="테스트 일시")

    class Meta:
        db_table = 'DIMC'
        verbose_name = 'DIMC 테스트 결과'
        verbose_name_plural = 'DIMC 테스트 결과 목록'

    def __str__(self):
        return f"DIMC Test {self.test_id} - {self.student.name}"





