# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.landing_pages import views



urlpatterns = [

    # services pages (level 3)
    path('services_profile/', views.services_profile, name='services_profile'),
    path('services_social_network/', views.services_social_network, name='services_social_network'),
    path('services_pinterest/', views.services_pinterest, name='services_pinterest'),
    path('services_youtube/', views.services_youtube, name='services_youtube'),
    path('services_instagram/', views.services_instagram, name='services_instagram'),
    path('services_facebook/', views.services_facebook, name='services_facebook'),
    path('services_twitter/', views.services_twitter, name='services_twitter'),
    # SEO hompage services pages (level 4)
    path('services_profile_category/', views.homepage_services_profile_category, name='services_profile_category'),
    path('services_social_category/', views.homepage_services_social_category, name='services_social_category'),
    path('services_linkedin_category/', views.homepage_services_linkedin_category, name='services_linkedin_category'),
    path('services_wikipedia_category/', views.homepage_services_wikipedia_category, name='services_wikipedia_category'),
    path('services_facebook_category/', views.homepage_services_facebook_category, name='services_facebook_category'),
    path('services_pinterest_category/', views.homepage_services_pinterest_category , name='services_pinterest_category'),
    path('services_amazon_category/', views.homepage_services_amazon_category, name='services_amazon_category'),
    path('services_twitter_category/', views.homepage_services_twitter_category, name='services_twitter_category'),
    path('services_spotify_category/', views.homepage_services_spotify_category, name='services_spotify_category'),

]
