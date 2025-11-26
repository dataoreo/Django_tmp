# course/urls.py

from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.course_list_view, name='course'),
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('create/', views.course_create_view, name='course_create'),
    path('<int:course_id>/update/', views.course_update_view, name='course_update'),
    path('<int:course_id>/delete/', views.course_delete_view, name='course_delete'),
]
