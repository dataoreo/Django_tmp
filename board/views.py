# board/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Notice, CommunityComment, CommunityBoard, CommunityPost
from .forms import NoticeForm, CommunityPostForm, CommunityCommentForm
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

@login_required
def community_view(request):
    return render(request, 'board/community_list.html')


# 1. 게시글 목록
def community_list(request):
    # 1. 모든 글 가져오기 (최신순)
    posts = CommunityPost.objects.all().order_by('-created_at')

    board_type = request.GET.get('board', '') # URL에서 '?board=xxx' 값을 가져옴
    if board_type:
        posts = posts.filter(board__board_type=board_type)

    filter_mode = request.GET.get('filter', '')
    if filter_mode == 'my' and request.user.is_authenticated:
        posts = posts.filter(author=request.user)

    # 2. 검색어 처리 (기존 코드 유지)
    q = request.GET.get('q', '')
    if q:
        posts = posts.filter(
            Q(post_title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__name__icontains=q)
        ).distinct()

    # 3. 페이지네이션 (기존 코드 유지)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # 번호 매기기 로직 (기존 코드 유지)
    if page_obj.paginator.count > 0:
        start_num = page_obj.paginator.count - page_obj.start_index() + 1
        for post in page_obj:
            post.number = start_num
            start_num -= 1

    context = {
        'posts': page_obj,
        'q': q,
        'board_type': board_type,
        'filter_mode': filter_mode,
    }
    return render(request, 'board/community_list.html', context)


# 2. 게시글 상세
def community_detail(request, post_id):
    post = get_object_or_404(CommunityPost, pk=post_id)

    if not post.open:
        if not request.user.is_authenticated:
            return redirect('board:community_list')

        if post.author != request.user and not request.user.is_manager():
            return redirect('board:community_list')

    # 조회수 증가 (본인 글이 아닐 때만 증가시키는 로직을 추가할 수도 있음)
    post.view += 1
    post.save()

    context = {'post': post}
    return render(request, 'board/community_detail.html', context)


# 3. 게시글 작성
@login_required
def community_create(request):
    if request.method == 'POST':
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:community_list')
    else:
        form = CommunityPostForm()

    return render(request, 'board/community_create.html', {'form': form})


# 4. 게시글 수정
@login_required
def community_update(request, post_id):
    post = get_object_or_404(CommunityPost, pk=post_id)

    # 작성자 본인 확인
    if post.author != request.user:
        return redirect('board:community_detail', post_id=post.post_id)

    if request.method == 'POST':
        form = CommunityPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('board:community_detail', post_id=post.post_id)
    else:
        form = CommunityPostForm(instance=post)

    return render(request, 'board/community_update.html', {'form': form, 'post': post})


# 5. 게시글 삭제
@login_required
def community_delete(request, post_id):
    post = get_object_or_404(CommunityPost, pk=post_id)

    if post.author == request.user or request.user.is_manager():
        if request.method == 'POST':
            post.delete()
            return redirect('board:community_list')
    else:
        return redirect('board:community_detail', post_id=post.post_id)

    # GET 요청이거나 작성자가 아니면 삭제 페이지(확인창) 보여주기
    return render(request, 'board/community_delete.html', {'post': post})


# 6. 댓글 작성
@login_required
def comment_create(request, post_id):
    post = get_object_or_404(CommunityPost, pk=post_id)

    if request.method == 'POST':
        form = CommunityCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(CommunityComment, pk=parent_id)
                comment.parent = parent_comment

            comment.save()

    return redirect('board:community_detail', post_id=post.post_id)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(CommunityComment, pk=comment_id)

    post_id = comment.post.post_id

    if request.user == comment.author or request.user.is_manager():
        comment.delete()
    else:
        return redirect('board:community_detail', post_id=post_id)

    return redirect('board:community_detail', post_id=post_id)