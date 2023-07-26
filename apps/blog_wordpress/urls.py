# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from .views import login_view, register_user, change_password_admin, activate_user, login_with_google, logout, resend_email_user_admin, udpate_remain_count_user_admin, change_password_user_admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout as auth_logout


urlpatterns = [
    path('blog2/', login_view, name="login"),
    
]
