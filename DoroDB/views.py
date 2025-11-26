from django.shortcuts import render
from board.models import Notice
from course.models import Course


def index_view(request):
    """홈페이지"""
    recent_notices = Notice.objects.all()[:5]
    recent_courses = Course.objects.filter(is_active=True)[:4]

    context = {
        'recent_notices': recent_notices,
        'recent_courses': recent_courses,
    }
    return render(request, 'index.html', context)