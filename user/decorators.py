# user/decorators.py

from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps


def staff_or_instructor_required(view_func):
    """강사 또는 관리자만 접근 가능한 데코레이터"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')

        # role이 instructor 또는 manager인 경우만 허용
        if request.user.role in ['instructor', 'manager']:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("⛔ 권한이 없습니다. 강사 또는 관리자만 접근 가능합니다.")

    return wrapper
