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
    path('key-phrases-extraction/', views.key_phrases_extraction, name='key_phrases_extraction'),
    path('named-entity-recognition/', views.named_entity_recognition, name='named_entity_recognition'),
    path('predict-customers-needs/', views.predict_customers_needs, name='predict_customers_needs'),
   
]
