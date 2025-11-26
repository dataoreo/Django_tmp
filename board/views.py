# board/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Notice
from .forms import NoticeForm
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


def notice_list_view(request):
    """공지사항 목록"""
    notices = Notice.objects.all()
    return render(request, 'board/notice_list.html', {'notices': notices})


def notice_detail_view(request, notice_id):
    """공지사항 상세"""
    notice = get_object_or_404(Notice, notice_id=notice_id)
    notice.views += 1
    notice.save()
    return render(request, 'board/notice_detail.html', {'notice': notice})


@login_required
@staff_or_instructor_required
def notice_create_view(request):
    """공지사항 작성"""
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('board:notice_detail', notice_id=notice.notice_id)
    else:
        form = NoticeForm()
    return render(request, 'board/notice_create.html', {'form': form})


@login_required
@staff_or_instructor_required
def notice_update_view(request, notice_id):
    """공지사항 수정"""
    notice = get_object_or_404(Notice, notice_id=notice_id)

    if notice.author != request.user:
        return HttpResponseForbidden("⛔ 본인이 작성한 글만 수정할 수 있습니다.")

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('board:notice_detail', notice_id=notice.notice_id)
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'board/notice_update.html', {'form': form, 'notice': notice})


@login_required
@staff_or_instructor_required
def notice_delete_view(request, notice_id):
    """공지사항 삭제"""
    notice = get_object_or_404(Notice, notice_id=notice_id)

    if notice.author != request.user:
        return HttpResponseForbidden("⛔ 본인이 작성한 글만 삭제할 수 있습니다.")

    if request.method == 'POST':
        notice.delete()
        return redirect('board:notice_list')

    return render(request, 'board/notice_delete.html', {'notice': notice})

