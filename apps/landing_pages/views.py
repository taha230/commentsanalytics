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
                    {'url': '/predict-customers-needs/', 'text': 'How to predict customers\' needs in their reviews'},
                    {'url': '/key-phrases-extraction/', 'text': 'Use key phrase extraction to quickly identify the main concepts in text'}

               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/The%20value%20of%20sentiment%20analysis%20in%20growing%20your%20business/', 'text': 'The value of sentiment analysis in growing your business'},
                    {'url': '/Post/Sentiment%20Analysis%20on%20YouTube%20Comments%20With%20Comments%20Analytics/', 'text': 'Sentiment Analysis on YouTube Comments With Comments Analytics'},
                    {'url': '/blog/machine-learning-and-classification/', 'text': 'MACHINE LEARNING AND CLASSIFICATION'.title()},
                    {'url': '/blog/text-processing-and-data-cleaning/', 'text': 'TEXT PROCESSING AND DATA CLEANING'.title()},
                    {'url': '/blog/sentiment-analysis-and-feedback/', 'text': 'SENTIMENT ANALYSIS AND FEEDBACK'.title()},
                    {'url': '/blog/text-analysis-and-nlp-techniques/', 'text': 'TEXT ANALYSIS AND NLP TECHNIQUES'.title()},
                    {'url': '/blog/keyword-extraction-and-data-collection/', 'text': 'KEYWORD EXTRACTION AND DATA COLLECTION'.title()},
               ]
              }

    return HttpResponse(html_template.render(context, request))

def key_phrases_extraction(request):
    html_template = loader.get_template('home/Landing_pages/key_phrases_extraction.html')

    context = {'title' : 'Keyword Extraction: A Guide to Finding Keywords in Text | NLP Keyword Extraction', 'description': 'Key Phrases Extraction is used to automatically pull out single keywords, or groups of two or more words to detect key phrases in unstructured text data.'
              ,'related_links' : [
                    {'url': '/sentiment-analysis/', 'text': 'Sentiment analysis tools to explore the customers\' emotions within the texts'},
                    {'url': '/predict-customers-needs/', 'text': 'How to predict customers\' needs in their reviews'}
               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/Keyword%20Extraction%20in%20Comments:%20Best%20Approach%20to%20Gain%20Insights%20from%20Your%20Customers/', 'text': 'Keyword Extraction in Comments: Best Approach to Gain Insights from Your Customers'},
                    {'url': '/blog/machine-learning-and-classification/', 'text': 'MACHINE LEARNING AND CLASSIFICATION'.title()},
                    {'url': '/blog/text-processing-and-data-cleaning/', 'text': 'TEXT PROCESSING AND DATA CLEANING'.title()},
                    {'url': '/blog/sentiment-analysis-and-feedback/', 'text': 'SENTIMENT ANALYSIS AND FEEDBACK'.title()},
                    {'url': '/blog/text-analysis-and-nlp-techniques/', 'text': 'TEXT ANALYSIS AND NLP TECHNIQUES'.title()},
                    {'url': '/blog/keyword-extraction-and-data-collection/', 'text': 'KEYWORD EXTRACTION AND DATA COLLECTION'.title()},
                    {'url': '/blog/word-cloud-and-visualization/', 'text': 'WORD CLOUD AND VISUALIZATION'.title()},
               ]
              }

    return HttpResponse(html_template.render(context, request))

def named_entity_recognition(request):
    html_template = loader.get_template('home/Landing_pages/named_entity_recognition.html')

    context = {'title' : 'Named Entity Recognition & Extraction API | NLP NER', 'description': 'Named entity recognition (NER) is an AI technique that automatically identifies key information in a text, like names of people, places, companies, and more.'
              ,'related_links' : [
                    {'url': '/key-phrases-extraction/', 'text': 'Use key phrase extraction to quickly identify the main concepts in text'}
               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/The%20value%20of%20sentiment%20analysis%20in%20growing%20your%20business/', 'text': 'The value of sentiment analysis in growing your business'},
                    {'url': '/blog/machine-learning-and-classification/', 'text': 'MACHINE LEARNING AND CLASSIFICATION'.title()},
                    {'url': '/blog/sentiment-analysis-and-feedback/', 'text': 'SENTIMENT ANALYSIS AND FEEDBACK'.title()},
                    {'url': '/blog/text-analysis-and-nlp-techniques/', 'text': 'TEXT ANALYSIS AND NLP TECHNIQUES'.title()},

                   ]
              }

    return HttpResponse(html_template.render(context, request))

def predict_customers_needs(request):
    html_template = loader.get_template('home/Landing_pages/predict_customers_needs.html')

    context = {'title' : 'Predict Customers Needs | AI tool', 'description': 'Predicting customer needs involves providing a service or product that customers haven\'t expressed a demand yet'
              ,'related_links' : [
                    {'url': '/key-phrases-extraction/', 'text': 'Use key phrase extraction to quickly identify the main concepts in text'},
                    {'url': '/sentiment-analysis/', 'text': 'Sentiment analysis tools to explore the customers\' emotions within the texts'}
               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/Keyword%20Extraction%20in%20Comments:%20Best%20Approach%20to%20Gain%20Insights%20from%20Your%20Customers/', 'text': 'Keyword Extraction in Comments: Best Approach to Gain Insights from Your Customers'},
                    {'url': '/blog/customer-surveys-and-feedback-loops/', 'text': 'CUSTOMER SURVEYS AND FEEDBACK LOOPS'.title()},
                    {'url': '/blog/text-analysis-and-nlp-techniques/', 'text': 'TEXT ANALYSIS AND NLP TECHNIQUES'.title()},

               ]
              }

    return HttpResponse(html_template.render(context, request))

def category_extraction(request):
    html_template = loader.get_template('home/Landing_pages/category_extraction.html')

    context = {'title' : 'Extract the Category of Comments', 'description': 'Extract comment categories to refine your reviews based on your preferences'
              ,'related_links' : [
                    {'url': '/key-phrases-extraction/', 'text': 'Use key phrase extraction to quickly identify the main concepts in text'},
                    {'url': '/sentiment-analysis/', 'text': 'Sentiment analysis tools to explore the customers\' emotions within the texts'}
               ]
               ,'related_posts' : 
               [
                    {'url': '/Post/YouTube%20Comments%20Categorizations:%20Benefits%20for%20YouTubers%20in%20User%20Answering,%20Engagement,%20and%20Satisfaction/', 'text': 'YouTube Comments Categorizations: Benefits for YouTubers in User Answering, Engagement, and Satisfaction'},
                    {'url': '/Post/Categorizing%20YouTube%20Comments:%20Unleashing%20the%20Power%20of%20Organization%20and%20Insight/', 'text': 'Categorizing YouTube Comments: Unleashing the Power of Organization and Insight'},
                    {'url': '/blog/machine-learning-and-classification/', 'text': 'MACHINE LEARNING AND CLASSIFICATION'.title()},
                    {'url': '/blog/text-processing-and-data-cleaning/', 'text': 'TEXT PROCESSING AND DATA CLEANING'.title()},
                    {'url': '/blog/sentiment-analysis-and-feedback/', 'text': 'SENTIMENT ANALYSIS AND FEEDBACK'.title()},
                    {'url': '/blog/text-analysis-and-nlp-techniques/', 'text': 'TEXT ANALYSIS AND NLP TECHNIQUES'.title()},

               ]
              }

    return HttpResponse(html_template.render(context, request))

