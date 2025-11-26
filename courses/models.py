from django.db import models
from user.models import User # user 앱의 User 모델 임포트

# 강의 정보
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100, verbose_name="강의명")
    # 강사만 선택 가능하도록 제한
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role': 'instructor'}, verbose_name="강사")
    start_date = models.DateField(null=True, blank=True, verbose_name="강의 시작일")
    end_date = models.DateField(null=True, blank=True, verbose_name="강의 종료일")

    class Meta:
        db_table = 'class'
        verbose_name = '강의'
        verbose_name_plural = '강의 목록'

    def __str__(self):
        return self.class_name

# 내 강의
class MyClass(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="강의")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, verbose_name="학생")

    class Meta:
        db_table = 'myclass'
        verbose_name = '수강 신청'
        verbose_name_plural = '수강 신청 목록'
        unique_together = ('class_obj', 'student') # 복합 기본 키 역할

    def __str__(self):
        return f"{self.student.name} - {self.class_obj.class_name}"

# 수강 진행 상태
class MyClassStatus(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, verbose_name="학생")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="강의")
    progress = models.IntegerField(default=0, verbose_name="진행도(%)")

    class Meta:
        db_table = 'myclass_status'
        verbose_name = '수강 진행 상태'
        verbose_name_plural = '수강 진행 상태 목록'
        unique_together = ('student', 'class_obj') # 복합 기본 키

    def __str__(self):
        return f"{self.student.name} - {self.class_obj.class_name}: {self.progress}%"

# 강의 평가
class SatisfactionSurvey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="강의")
    title = models.CharField(max_length=100, verbose_name="설문조사 제목")
    start_date = models.DateTimeField(verbose_name="강의평가 시작 기간")
    end_date = models.DateTimeField(verbose_name="강의평가 종료 기간")

    class Meta:
        db_table = 'satisfaction_survey'
        verbose_name = '강의 만족도 조사'
        verbose_name_plural = '강의 만족도 조사 목록'

    def __str__(self):
        return self.title

# 설문조사 질문 항목
class SurveyQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(SatisfactionSurvey, on_delete=models.CASCADE, verbose_name="설문조사")
    question = models.CharField(max_length=255, verbose_name="질문 내용")
    question_type = models.CharField(max_length=20, verbose_name="질문 유형")
    question_num = models.IntegerField(verbose_name="질문 번호")

    class Meta:
        db_table = 'survey_question'
        verbose_name = '설문조사 질문'
        verbose_name_plural = '설문조사 질문 목록'

    def __str__(self):
        return f"{self.survey.title} - Q{self.question_num}"

# 학생 응답 (설문 제출)
class SurveySubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(SatisfactionSurvey, on_delete=models.CASCADE, verbose_name="설문조사")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, verbose_name="학생")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="제출 일시")

    class Meta:
        db_table = 'survey_submission'
        verbose_name = '설문조사 제출'
        verbose_name_plural = '설문조사 제출 목록'
        unique_together = ('survey', 'student')

    def __str__(self):
        return f"{self.survey.title} 제출 - {self.student.name}"

# 응답 결과
class SurveyAnswer(models.Model):
    result_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, verbose_name="제출 ID")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, verbose_name="질문 ID")
    answer_value = models.TextField(max_length=255, verbose_name="응답값")

    class Meta:
        db_table = 'survey_answer'
        verbose_name = '설문조사 응답'
        verbose_name_plural = '설문조사 응답 목록'
        unique_together = ('submission', 'question')

    def __str__(self):
        return f"응답: {self.question.question_num}번 질문"

# 강의 게시판
class ClassBoard(models.Model):
    board_id = models.AutoField(primary_key=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="강의")
    board_name = models.CharField(max_length=100, verbose_name="게시판 이름")
    board_type = models.CharField(max_length=20, verbose_name="게시판 유형")

    class Meta:
        db_table = 'class_board'
        verbose_name = '강의 게시판'
        verbose_name_plural = '강의 게시판 목록'

    def __str__(self):
        return f"{self.class_obj.class_name} - {self.board_name}"

# 강의 게시글
class ClassPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    board = models.ForeignKey(ClassBoard, on_delete=models.CASCADE, verbose_name="게시판")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")
    open = models.BooleanField(default=True, verbose_name="공개 여부")
    view_count = models.IntegerField(default=0, verbose_name="조회수")

    class Meta:
        db_table = 'class_post'
        verbose_name = '강의 게시글'
        verbose_name_plural = '강의 게시글 목록'

    def __str__(self):
        return self.title

# 강의 댓글
class ClassComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(ClassPost, on_delete=models.CASCADE, verbose_name="게시글")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    comment_content = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'class_comment'
        verbose_name = '강의 댓글'
        verbose_name_plural = '강의 댓글 목록'

    def __str__(self):
        return f"{self.author.name}의 댓글 ({self.post.title})"

# 강의 자료 파일
class MaterialFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(ClassPost, on_delete=models.CASCADE, verbose_name="게시글")
    file_name = models.CharField(max_length=100, verbose_name="파일명")
    file_path = models.TextField(verbose_name="파일 경로")
    file_size = models.IntegerField(verbose_name="파일 크기")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="업로드 일시")

    class Meta:
        db_table = 'material_file'
        verbose_name = '강의 자료 파일'
        verbose_name_plural = '강의 자료 파일 목록'

    def __str__(self):
        return self.file_name