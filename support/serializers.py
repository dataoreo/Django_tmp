from rest_framework import serializers
from .models import FAQCategory, FAQItem

class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'depth']  # JS의 opt.name과 매칭

class FAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = ['id', 'question', 'answer'] # JS의 opt.question, opt.answer와 매칭