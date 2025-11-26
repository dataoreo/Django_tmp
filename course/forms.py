# course/forms.py

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '강의명을 입력하세요',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': '강의 설명을 입력하세요',
                'rows': 10,
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'is_active': forms.CheckboxInput()
        }
        labels = {
            'title': '강의명',
            'description': '강의 설명',
            'is_active': '활성화'
        }
