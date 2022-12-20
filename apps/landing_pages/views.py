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


############################################# Uploaded Images ###########################################################

def email_banners(request):
     image_data = open('apps/static/assets/img/upload_images/email_banner.png', mode='rb').read()
     return HttpResponse(image_data, content_type="image/png")

############################################# Services Pages ###########################################################

def sentiment_analysis(request):
    html_template = loader.get_template('home/Landing_pages/sentiment_analysis.html')

    context = {'title' : 'Sentiment Analysis API & Emotion Mining Tool | NLP API', 'description': 'Analyze, detect, and monitor the sentiment hidden in your unstructured data with the best NLP-based sentiment analysis API.'
              ,'related_links' : [
                    {'url': '', 'text': ''}
               ]
               ,'related_posts' : 
               [
                    {'url': '', 'text': ''}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def key_phrases_extraction(request):
    html_template = loader.get_template('home/Landing_pages/key_phrases_extraction.html')

    context = {'title' : 'Keyword Extraction: A Guide to Finding Keywords in Text | NLP Keyword Extraction', 'description': 'Key Phrases Extraction is used to automatically pull out single keywords, or groups of two or more words to detect key phrases in unstructured text data.'
              ,'related_links' : [
                    {'url': '', 'text': ''}
               ]
               ,'related_posts' : 
               [
                    {'url': '', 'text': ''}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def named_entity_recognition(request):
    html_template = loader.get_template('home/Landing_pages/named_entity_recognition.html')

    context = {'title' : 'Named Entity Recognition & Extraction API | NLP NER', 'description': 'Named entity recognition (NER) is an AI technique that automatically identifies key information in a text, like names of people, places, companies, and more.'
              ,'related_links' : [
                    {'url': '', 'text': ''}
               ]
               ,'related_posts' : 
               [
                    {'url': '', 'text': ''}
               ]
              }

    return HttpResponse(html_template.render(context, request))

def predict_customers_needs(request):
    html_template = loader.get_template('home/Landing_pages/predict_customers_needs.html')

    context = {'title' : 'Sentiment Analysis API & Emotion Mining Tool | NLP API', 'description': 'Analyze, detect, and monitor the sentiment hidden in your unstructured data with the best NLP-based sentiment analysis API from Repustate.'
              ,'related_links' : [
                    {'url': '', 'text': ''}
               ]
               ,'related_posts' : 
               [
                    {'url': '', 'text': ''}
               ]
              }

    return HttpResponse(html_template.render(context, request))

