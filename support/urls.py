# support/urls.py
from django.urls import path
from .views import ChatbotFlowView, chatbot_page

urlpatterns = [
    # 화면 주소: /support/chatbot/
    path('', chatbot_page, name='support-root'),
    path('chatbot/', chatbot_page, name='chatbot-ui'),

    # API 주소: /support/api/chatbot/
    path('api/chatbot/', ChatbotFlowView.as_view(), name='chatbot-api'),
]
