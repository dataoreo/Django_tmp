"""
ASGI config for 데이터베이스 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoroDB.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
import chat.routing

# HTTP 연결을 Django의 기본 ASGI 핸들러로 라우팅
# WebSocket 연결은 AuthMiddlewareStack과 URLRouter를 거치도록 설정
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # WebSocket 요청이 들어오면 인증 미들웨어와 chat.routing의 URLRouter를 통해 Consumer로 전달됩니다.
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})