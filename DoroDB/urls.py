"""
URL configuration for 데이터베이스 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #루트 페이지
    path('', views.index_view, name='index'),
    # user/로 시작하는 모든 url은 user.urls에서 처리
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('board/', include('board.urls')),
    path('course/', include('course.urls')),
    path('support/', include('support.urls')),
]

# 개발 환경에서 미디어 파일을 서빙하기 위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)