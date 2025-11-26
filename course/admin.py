# course/admin.py

from django.contrib import admin
from .models import Course
from django.utils.html import format_html


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'title', 'instructor', 'status_badge', 'views', 'created_date']
    list_filter = ['is_active', 'created_at', 'instructor']
    search_fields = ['title', 'description', 'instructor__name', 'instructor__email']
    ordering = ['-created_at']
    readonly_fields = ['course_id', 'views', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('기본 정보', {
            'fields': ('course_id', 'instructor', 'title', 'description')
        }),
        ('설정', {
            'fields': ('is_active', 'views')
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">활성</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">비활성</span>'
        )

    status_badge.short_description = '상태'

    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_date.short_description = '등록일'
    created_date.admin_order_field = 'created_at'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)
