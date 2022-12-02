# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from termcolor import colored
from django.contrib.auth.models import User
# from authentication import CustomUser
from apps.authentication.views import send_email_from_admin_to_client, send_email_from_client_to_admin
import datetime
import requests
import uuid
import json
from django.contrib.sites.shortcuts import get_current_site
import smtplib
import csv
from xlsxwriter.workbook import Workbook
import openpyxl
import time
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse
from reportlab.lib.colors import pink, green, brown, white, black, red, gray
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.units import mm
# from reportlab.platypus import Image
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.utils import ImageReader
import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
import gevent
from multiprocessing import Manager
import multiprocessing
from pymongo import MongoClient
from bson.objectid import ObjectId


############################################# Services Pages ###########################################################

def email_banners(request):
     image_data = open('apps/static/assets/img/upload_images/email_banner.png', mode='rb').read()
     return HttpResponse(image_data, content_type="image/png")
     
def services_profile(request):
    html_template = loader.get_template('home/Landing_pages/services_profile.html')

    context = {'title' : 'profile account', 'description': 'Finding profile urls of people, business and ... in popular websites'
              ,'related_links' : [
                    {'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
                    ,{'url': '/Post/Zoominfo%20service%20is%20accesible/', 'text': 'Zoominfo service is accesible'}
                    ,{'url': '/Post/Crunchbase%20Profile%20URL%20finder%20added!/', 'text': 'Crunchbase Profile URL finder added'}
                    ,{'url': '/Post/Wikipedia%20began%20in%20the%20West%20but%20is%20now%20growing%20in%20the%20global%20South/', 'text': 'Wikipedia began in the West but is now growing in the global South'}
                    ,{'url': '/Post/Amazon%20profile%20page%20finder%20service%20has%20launched/', 'text': 'Amazon profile page finder service has launched'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_social_network(request):
    html_template = loader.get_template('home/Landing_pages/services_social_network.html')

    context = {'title' : 'social media urls', 'description': 'Extracting the URLs of social network URLs. The social networks such as Twitter, Facebook, Instagram and Youtbe.'
              ,'related_links' : [
                    {'url': '/services_pinterest/', 'text': 'Extracting profile of product proivders in Pinterest'}
                    ,{'url': '/services_youtube/', 'text': 'Finding Youtubers and Companies Youtube channel profile URL'}
                    ,{'url': '/services_instagram/', 'text': 'Person, Business, Influencer Instagram profile URLs finder Services'}
                    ,{'url': '/services_profile/', 'text': 'Person, Business, Blogging or other General profile URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Using%20social%20network%20profiles%20for%20lead%20generation%20of%20your%20business/', 'text': 'Using social network profiles for lead generation of your business'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Meta%20company%20has%20hired%20its%20first-ever%20VP%20of%20Civil%20Rights/', 'text': 'Meta company has hired its first-ever VP of Civil Rights'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_pinterest(request):
    html_template = loader.get_template('home/Landing_pages/services_pinterest.html')

    context = {'title' : 'pinterest profile link', 'description': 'Extracting the URLs of Pinterest Profiles. Pinterest is an image sharing and social media service designed to enable saving and discovery of information on the internet using images, and on a smaller scale, animated GIFs and videos, in the form of pinboards.'
              ,'related_links' : [
                    {'url': '/services_profile/', 'text': 'Person, Business, Blogging or other General profile URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20marketing%20on%20Pinterest/', 'text': 'Business marketing on Pinterest'}
                    ,{'url': '/Post/Free%20plan:%20Best%20approach%20to%20attract%20customers%20to%20purchase/', 'text': 'Free plan: Best approach to attract customers to purchase'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Hiring%20the%20ideal%20candidate%20by%20profile%20analysis/', 'text': 'Hiring the ideal candidate by profile analysis'}
                    ,{'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_youtube(request):
    html_template = loader.get_template('home/Landing_pages/services_youtube.html')

    context = {'title' : 'youtube profile link', 'description': 'Extracting the URLs of Youtube Profiles. '
              ,'related_links' : [
                    {'url': '/services_profile/', 'text': 'Person, Business, Blogging or other General profile URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Free%20plan:%20Best%20approach%20to%20attract%20customers%20to%20purchase/', 'text': 'Free plan: Best approach to attract customers to purchase'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_instagram(request):
    html_template = loader.get_template('home/Landing_pages/services_instagram.html')

    context = {'title' : 'instagram profile link', 'description': 'Extracting the URLs of Instagram Profiles. '
              ,'related_links' : [
                    {'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterset/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_youtube/', 'text': 'Youtube URLs finder of Youtuber and Companies'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Free%20plan:%20Best%20approach%20to%20attract%20customers%20to%20purchase/', 'text': 'Free plan: Best approach to attract customers to purchase'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_facebook(request):
    html_template = loader.get_template('home/Landing_pages/services_facebook.html')

    context = {'title' : 'how to get facebook profile link', 'description': 'Extracting the URLs of Facebook Profiles. how to get facebook profile link?'
              ,'related_links' : [
                    {'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterset/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_youtube/', 'text': 'Youtube URLs finder of Youtuber and Companies'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Meta%20company%20has%20hired%20its%20first-ever%20VP%20of%20Civil%20Rights/', 'text': 'Meta company has hired its first-ever VP of Civil Rights'}
                    ,{'url': '/Post/Free%20plan:%20Best%20approach%20to%20attract%20customers%20to%20purchase/', 'text': 'Free plan: Best approach to attract customers to purchase'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def services_twitter(request):
    html_template = loader.get_template('home/Landing_pages/services_twitter.html')

    context = {'title' : 'how to get twitter profile link', 'description': 'Extracting the URLs of twitter Profiles. how to get twitter profile link?'
              ,'related_links' : [
                    {'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_pinterset/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_youtube/', 'text': 'Youtube URLs finder of Youtuber and Companies'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Free%20plan:%20Best%20approach%20to%20attract%20customers%20to%20purchase/', 'text': 'Free plan: Best approach to attract customers to purchase'}
                    ,{'url': '/Post/Bulk%20Requests%20needs%20for%20saving%20your%20time%20for%20large%20files/', 'text': 'Bulk Requests needs for saving your time for large files'}
                    ,{'url': '/Post/Single%20Request%20option%20to%20validate%20the%20quality%20of%20URL%20finding%20services/', 'text': 'Single Request option to validate the quality of URL finding services'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
                    ,{'url': '/Post/Company%20Verification%20using%20social%20media%20accounts/', 'text': 'Company Verification using social media accounts'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor as a need for social marketers and growing your business'}
                    ,{'url': '/Post/Large%20data%20import%20as%20csv%20and%20xlsx%20format%20in%20the%20Bulk%20Requests%20mode/', 'text': 'Large data import as csv and xlsx format in the Bulk Requests mode'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def homepage_services_profile_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-profile_url.html')

    context = {'title' : 'profile account', 'description': 'Finding profile urls of people, business and ... in popular websites'
              ,'related_links' : [
                    {'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
                    ,{'url': '/Post/Zoominfo%20service%20is%20accesible/', 'text': 'Zoominfo service is accesible'}
                    ,{'url': '/Post/Crunchbase%20Profile%20URL%20finder%20added!/', 'text': 'Crunchbase Profile URL finder added'}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def homepage_services_social_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-social_url.html')

    context = {'title' : 'social media links', 'description': 'Extracting all social network popular accounts'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
                    ,{'url': '/Post/Zoominfo%20service%20is%20accesible/', 'text': 'Zoominfo service is accesible'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}
                    ,{'url': '/Post/Why%20you%20should%20start%20monitoring%20your%20business%20competitors%20in%20social%20networks/', 'text': 'Why you should start monitoring your business competitors in social networks'}
               ]}
    return HttpResponse(html_template.render(context, request))

def homepage_services_linkedin_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-linkedin_url.html')

    context = {'title' : 'how to get linkedin url', 'description': 'Finding Linkedin profile of employees and employers'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
                    ,{'url': '/Post/Zoominfo%20service%20is%20accesible/', 'text': 'Zoominfo service is accesible'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}
               ]}

    return HttpResponse(html_template.render(context, request))

def homepage_services_wikipedia_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-wikipedia_url.html')

    context = {'title' : 'wikipedia search url', 'description': 'Finding Wikipedia profile of entities including general information pages'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Wikipedia%20began%20in%20the%20West%20but%20is%20now%20growing%20in%20the%20global%20South/', 'text': 'Wikipedia began in the West but is now growing in the global South'},
                    {'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}

               ]}

    return HttpResponse(html_template.render(context, request))

def homepage_services_facebook_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-facebook_url.html')

    context = {'title' : 'how to find facebook profile link', 'description': 'Finding Facebook profile of users and organizations'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Meta%20company%20has%20hired%20its%20first-ever%20VP%20of%20Civil%20Rights/', 'text': 'Meta company has hired its first-ever VP of Civil Rights'},
                    {'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}      
               ]}
    
    return HttpResponse(html_template.render(context, request))

def homepage_services_pinterest_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-pinterest_url.html')

    context = {'title' : 'how to get pinterest profile link', 'description': 'Finding Pinterest profile of designers'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20marketing%20on%20Pinterest/', 'text': 'Business marketing on Pinterest'}
                    ,{'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
               ]}
    
    return HttpResponse(html_template.render(context, request))

def homepage_services_amazon_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-amazon_url.html')

    context = {'title' : 'how to find my amazon profile link', 'description': 'Finding Amazon page of products and sellers'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Amazon%20profile%20page%20finder%20service%20has%20launched/', 'text': 'Amazon profile page finder service has launched'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}
               ]}
    
    return HttpResponse(html_template.render(context, request))

def homepage_services_twitter_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-twitter_url.html')

    context = {'title' : 'how to get twitter profile link', 'description': 'Finding Twitter profile of people, Business and Influencers, ...'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_spotify_category/', 'text': 'Spotify URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Business%20Profiles%20monitoring%20as%20a%20need%20for%20companies/', 'text': 'Business Profiles monitoring as a need for companies'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}
               ]}
    
    return HttpResponse(html_template.render(context, request))

def homepage_services_spotify_category(request):
    html_template = loader.get_template('home/Landing_pages/homepage-spotify_url.html')

    context = {'title' : 'spotify artist account', 'description': 'Finding Spotify profile of artists'
              ,'related_links' : [
                     {'url': '/services_profile_category/', 'text': 'Profile URLs finder Services '}
                    ,{'url': '/services_social_category/', 'text': 'Social Network URLs finder Services'}
                    ,{'url': '/services_wikipedia_category/', 'text': 'Wikipedia URLs finder Services'}
                    ,{'url': '/services_facebook_category/', 'text': 'Facebook URLs finder Services'}
                    ,{'url': '/services_pinterest_category/', 'text': 'Pinterest URLs finder Services'}
                    ,{'url': '/services_amazon_category/', 'text': 'Amazon URLs finder Services'}
                    ,{'url': '/services_twitter_category/', 'text': 'Twitter URLs finder Services'}
                    ,{'url': '/services/', 'text': 'Profile browse Services'}
               ]
               ,'related_posts' : [
                    {'url': '/Post/Spotify%20has%20the%20largest%20music%20library%20in%20the%20world/', 'text': 'Spotify has the largest music library in the world'}
                    ,{'url': '/Post/Social%20network%20accounts%20extractor%20as%20a%20need%20for%20social%20marketers%20and%20growing%20your%20business/', 'text': 'Social network accounts extractor for social marketers and growing your business'}
               ]}
    
    return HttpResponse(html_template.render(context, request))
