#board.urls

from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('notice/', views.notice_list_view, name='notice_list'),
    path('notice/<int:notice_id>/', views.notice_detail_view, name='notice_detail'),
    path('notice/create/', views.notice_create_view, name='notice_create'),
    path('notice/<int:notice_id>/update/', views.notice_update_view, name='notice_update'),
    path('notice/<int:notice_id>/delete/', views.notice_delete_view, name='notice_delete'),

    path('community/', views.community_list, name='community_list'),
    path('community/create/', views.community_create, name='community_create'),
    path('community/<int:post_id>/', views.community_detail, name='community_detail'),
    path('community/<int:post_id>/update/', views.community_update, name='community_update'),
    path('community/<int:post_id>/delete/', views.community_delete, name='community_delete'),
    path('community/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('community/comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),

]
