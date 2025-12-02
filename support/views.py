from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import FAQCategory, FAQItem
from .serializers import FAQCategorySerializer, FAQItemSerializer


# 1. 화면 렌더링 (HTML 보여주기)
def chatbot_page(request):
    return render(request, 'support/chatbot.html')


# 2. API 로직 (데이터 보내주기)
class ChatbotFlowView(APIView):
    """
    [GET] /api/support/chatbot/?parent_id=...
    """

    def get(self, request):
        # parent_id가 없으면 None (최상위 카테고리 조회)
        parent_id = request.query_params.get('parent_id')

        # 'null' 문자열로 들어오는 경우 처리 (JS fetch에서 null을 보낼 때 대비)
        if parent_id == 'null' or parent_id == '':
            parent_id = None

        # 1. 하위 카테고리가 있는지 확인 (폴더 구조)
        sub_categories = FAQCategory.objects.filter(parent_id=parent_id)

        if sub_categories.exists():
            return Response({
                "type": "category",  # HTML JS가 아이콘(📂)을 결정하는 값
                "message": "원하시는 항목을 선택해 주세요.",
                "data": FAQCategorySerializer(sub_categories, many=True).data
            }, status=status.HTTP_200_OK)

        # 2. 하위 카테고리가 없으면 -> 질문 리스트 확인
        questions = FAQItem.objects.filter(category_id=parent_id)

        if questions.exists():
            return Response({
                "type": "question",  # HTML JS가 아이콘(❓)을 결정하는 값
                "message": "아래 질문 중에서 선택해 주세요.",
                "data": FAQItemSerializer(questions, many=True).data
            }, status=status.HTTP_200_OK)

        # 3. 데이터가 아예 없는 경우
        return Response({
            "type": "empty",
            "message": "등록된 내용이 없습니다.",
            "data": []
        }, status=status.HTTP_200_OK)