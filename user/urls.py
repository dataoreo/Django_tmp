# user/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    # 회원가입 경로
    path('term/', views.term_view, name='term'),
    path('signup/', views.signup_view, name='signup'),
    path('complete/', views.signup_complete_view, name='signup_complete'),

    # 👇 [추가] 이메일 인증 경로
    path('verify-email/<uuid:token>/', views.verify_email_view, name='verify_email'),

    # 로그인 및 로그아웃 경로
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 마이페이지
    path('mypage/', views.mypage_view, name='mypage'),
    path('mypage/update/', views.mypage_update_view, name='mypage_update'),
    path('mypage/delete/', views.user_delete_view, name='mypage_delete'),

    # DIMC
    path('DIMC', views.DIMC_view, name='DIMC'),
    path('DIMC_archive', views.DIMC_archive_view, name='DIMC_archive'),

    path('community/', views.community_view, name='community' ),
    path('course/', views.dashboard_view, name='dashboard' ),
    path('calendar/', views.calendar_view, name='main_calendar'),
    path('course/info/<int:class_id>', views.lecture_info_view, name='lecture_info'),
    path('course/register/', views.course_registration_view, name='course_register'),
    path('archive/instructor/', views.instructor_archive_view, name='instructor_archive'),
    path('course/', views.courses_view, name='courses' ),

    path('find_id/', views.find_id_view, name='find_id'),
    # 👇 비밀번호 재설정 절차 (URL 경로 수정)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset_form.html',
             email_template_name='user/password_reset_email.html',
             success_url='/user/password-reset/done/'),  # 👈 하이픈(-) 사용
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',  # 👈 하이픈(-) 사용
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html',
             success_url='/user/password-reset-complete/'),  # 👈 하이픈(-) 사용
         name='password_reset_confirm'),

    path('password-reset-complete/',  # 👈 하이픈(-) 사용
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),



]
