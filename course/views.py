# course/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course
from .forms import CourseForm
from functools import wraps


def staff_or_instructor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')

        if request.user.role in ['instructor', 'manager']:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("⛔ 권한이 없습니다.")

    return wrapper


def course_list_view(request):
    """강의 목록"""
    courses = Course.objects.filter(is_active=True)
    return render(request, 'course/course.html', {'courses': courses})


def course_detail_view(request, course_id):
    """강의 상세"""
    course = get_object_or_404(Course, course_id=course_id)
    course.views += 1
    course.save()
    return render(request, 'course/course_detail.html', {'course': course})


@login_required
@staff_or_instructor_required
def course_create_view(request):
    """강의 등록"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course:course_detail', course_id=course.course_id)
    else:
        form = CourseForm()
    return render(request, 'course/course_create.html', {'form': form})


@login_required
@staff_or_instructor_required
def course_update_view(request, course_id):
    """강의 수정"""
    course = get_object_or_404(Course, course_id=course_id)

    if course.instructor != request.user:
        return HttpResponseForbidden("⛔ 본인이 등록한 강의만 수정할 수 있습니다.")

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course:course_detail', course_id=course.course_id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'course/course_update.html', {'form': form, 'course': course})


@login_required
@staff_or_instructor_required
def course_delete_view(request, course_id):
    """강의 삭제"""
    course = get_object_or_404(Course, course_id=course_id)

    if course.instructor != request.user:
        return HttpResponseForbidden("⛔ 본인이 등록한 강의만 삭제할 수 있습니다.")

    if request.method == 'POST':
        course.delete()
        return redirect('course:course')

    return render(request, 'course/course_delete.html', {'course': course})
