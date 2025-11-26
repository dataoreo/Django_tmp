# board/admin.py

from django.contrib import admin
from .models import Notice
from django.utils.html import format_html


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['notice_id', 'title_with_badge', 'author', 'views', 'created_date']
    list_filter = ['is_pinned', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__name', 'author__email']
    ordering = ['-is_pinned', '-created_at']
    readonly_fields = ['notice_id', 'views', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('기본 정보', {
            'fields': ('notice_id', 'author', 'title', 'content')
        }),
        ('설정', {
            'fields': ('is_pinned', 'views')
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def title_with_badge(self, obj):
        if obj.is_pinned:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-right: 5px;">고정</span> {}',
                obj.title
            )
        return obj.title

    title_with_badge.short_description = '제목'

    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_date.short_description = '작성일'
    created_date.admin_order_field = 'created_at'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
