# user/forms.py
from django import forms
from .models import User,DIMC

# 👇 필요한 모듈 추가
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# 약관 동의를 위한 폼
class TermsForm(forms.Form):
    # '동의' 체크박스 필드. 필수로 체크해야 함
    agree = forms.BooleanField(
        label='[필수] 서비스 이용약관에 동의합니다.',
        error_messages={'required': '약관에 동의하셔야 회원가입을 진행할 수 있습니다.'}
    )


# 회원 정보 입력
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'name', 'phone_number', 'address', 'birthday', 'code']
        widgets = {
            'password': forms.PasswordInput,
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password:
            # 👇 Django의 비밀번호 유효성 검사 실행
            try:
                validate_password(password)
            except ValidationError as e:
                # 에러 메시지를 password 필드에 추가
                self.add_error('password', e)

            # 비밀번호 일치 여부 확인
            if password_confirm and (password != password_confirm):
                self.add_error('password_confirm', '비밀번호가 일치하지 않습니다.')

        return cleaned_data



class DimcTestForm(forms.ModelForm):
    class Meta:
        model = DIMC
        # 사용자로부터 직접 입력받을 필드만 지정합니다.
        # 'student'와 'tested_at'은 뷰에서 자동으로 처리되므로 제외합니다.
        fields = ['D_score', 'I_score', 'M_score', 'C_score', 'result', 'pdf_path']
        labels = {
            'D_score': 'D 점수',
            'I_score': 'I 점수',
            'M_score': 'M 점수',
            'C_score': 'C 점수',
            'result': '테스트 결과 요약',
            'pdf_path': 'PDF 파일 경로',
        }


# user/forms.py 에 아래 클래스 추가
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # 👇 fields 리스트에 'profile_image' 추가
        fields = ['name', 'phone_number', 'address', 'birthday', 'profile_image']
        labels = {
            'name': '이름',
            'phone_number': '전화번호',
            'address': '주소',
            'birthday': '생년월일',
            'profile_image': '프로필 사진 URL', # 👈 라벨 변경
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            # 👇 profile_image 필드를 여러 줄 입력 가능한 텍스트 박스로 변경

        }

class DIMCForm(forms.ModelForm):
    class Meta:
        model = DIMC
        fields = ['D_score', 'I_score', 'M_score', 'C_score', 'result','pdf_path']#복구시 resurlt 넣어야됨
        widgets = {
            'D_score': forms.NumberInput(attrs={'min': 0}),
            'I_score': forms.NumberInput(attrs={'min': 0}),
            'M_score': forms.NumberInput(attrs={'min': 0}),
            'C_score': forms.NumberInput(attrs={'min': 0}),
            'result': forms.Textarea(attrs={'rows': 0}),
            'pdf_path': forms.ClearableFileInput(attrs={'placeholder': 'PDF 파일 경로를 입력하세요'}),
        }






