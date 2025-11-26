# board/urls.py

from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('notice/', views.notice_list_view, name='notice_list'),
    path('notice/<int:notice_id>/', views.notice_detail_view, name='notice_detail'),
    path('notice/create/', views.notice_create_view, name='notice_create'),
    path('notice/<int:notice_id>/update/', views.notice_update_view, name='notice_update'),
    path('notice/<int:notice_id>/delete/', views.notice_delete_view, name='notice_delete'),
]
