# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from .views import login_view, register_user, change_password_admin, activate_user, login_with_google, logout, resend_email_user_admin, udpate_remain_count_user_admin, change_password_user_admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout as auth_logout


urlpatterns = [
    path('login/', login_view, name="login"),
    # path('blog2/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('change_password_admin/', change_password_admin, name="change_password_admin"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path("logout/", logout, name="logout"),
    re_path(r'activate_user_', activate_user, name="activate_user"),
    path('accounts/', include('allauth.urls')),
    re_path(r'^login_with_google', login_with_google, name="login_with_google"),
    re_path(r'^resend_email_user_admin/user_', resend_email_user_admin, name="resend_email_user_admin"), # use regular expression for handle all pages /user_*
    re_path(r'^udpate_remain_count_user_admin/user_', udpate_remain_count_user_admin, name="udpate_remain_count_user_admin"), # use regular expression for handle all pages /user_*
    re_path(r'^change_password_user_admin/user_', change_password_user_admin, name="change_password_user_admin"), # use regular expression for handle all pages /user_*
]
