# board/forms.py

from django import forms
from .models import Notice

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
