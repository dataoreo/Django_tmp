# board/forms.py

from django import forms
from .models import Notice
from .models import CommunityPost, CommunityComment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '제목을 입력하세요',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': '내용을 입력하세요',
                'rows': 10,
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'is_pinned': forms.CheckboxInput()
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'is_pinned': '상단 고정'
        }


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        # 👇 [수정 1] fields 리스트 맨 앞에 'board' 추가
        fields = ['board', 'post_title', 'content', 'open']

        widgets = {
            # 👇 [수정 2] 드롭다운 스타일링을 위한 위젯 추가
            'board': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 5px;'
            }),
            'post_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요',
                'style': 'width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 5px;'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력하세요',
                'style': 'width: 100%; height: 300px; padding: 10px; border: 1px solid #dee2e6; border-radius: 5px; resize: none;'
            }),
            'open': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 18px; height: 18px;'
            }),
        }
        # 👇 [선택 사항] 라벨 명시 (필요 시)
        labels = {
            'board': '게시판 분류',
            'post_title': '제목',
            'content': '내용',
            'open': '공개 여부',
        }

class CommunityCommentForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['comment_content']