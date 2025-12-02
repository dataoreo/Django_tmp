from django.contrib import admin
from .models import FAQCategory, FAQItem

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'depth', 'parent']
    list_filter = ['depth']

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'category']
    list_filter = ['category']
