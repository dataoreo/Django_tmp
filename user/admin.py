from django.contrib import admin

# Register your models here.
# user/admin.py
from django.contrib import admin
from .models import User, DIMC # User와 DIMC 모델을 불러옵니다.

# 관리자 페이지에 User 모델을 등록합니다.
admin.site.register(User)
# 관리자 페이지에 DIMC 모델을 등록합니다.
admin.site.register(DIMC)