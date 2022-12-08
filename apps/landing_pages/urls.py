# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.landing_pages import views



urlpatterns = [

    # upload images URLs
    path('email_banners.png', views.email_banners, name='email_banners'),

    # services pages (level 2)
    path('sentiment-analysis/', views.sentiment_analysis, name='sentiment_analysis'),
   
]
