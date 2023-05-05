import flask
import os.path
from termcolor import colored
import validators
import json
import requests
from bs4 import BeautifulSoup
import random
import multiprocessing
import re
from multiprocessing import Pool, Value
import queue
from itertools import groupby
import string
from enum import Enum
import time
from pymongo import MongoClient
import pickle
import datetime
import yarl
import bson
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
# import spacy
# from keybert import KeyBERT
import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.classification import ClassificationModel
import torch
import logging
# from simpletransformers.model import CustomModel
from transformers import AutoModel
from transformers import pipeline
import spacy
from keybert import KeyBERT

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

model_path = "outputs/model_args.json"
sentiment_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")


# model_youtube = ClassificationModel(
# "roberta", "outputs", use_cuda=False, args={'reprocess_input_data': True,
#                                   'overwrite_output_dir': True,
#                                   'use_multiprocessing': False,
#                                   'num_train_epochs': 10,
#                                   'learning_rate': 3e-5,
#                                   'train_batch_size': 4,
#                                   'eval_batch_size': 1,
#                                   'gradient_accumulation_steps': 1,
#                                   'save_steps': 1000,
#                                   'fp16': False}
# )

model_youtube = None

def get_model():
    global model_youtube
    if model_youtube is None:
        model_args = args={'reprocess_input_data': True,
                                  'overwrite_output_dir': True,
                                  "use_multiprocessing": False, "use_multiprocessing_for_evaluation": False, "process_count": 1,
                                  'num_train_epochs': 10,
                                  'learning_rate': 3e-5,
                                  'train_batch_size': 4,
                                  'eval_batch_size': 1,
                                  'gradient_accumulation_steps': 1,
                                  'save_steps': 1000,
                                  'fp16': False}
        model_youtube = ClassificationModel('roberta', "outputs", use_cuda=False, args=model_args)
    return model_youtube


youtube_categories_json = {
    'Feedback' : 0,
    'Functionality' : 1,
    'Personal Experience' : 2,
    'Pricing' : 3,
    'Question' : 4,
    'Suggestion' : 5,
    'Others' : 6

}

application = flask.Flask(__name__)

application.config["DEBUG"] = True

##########################################################

def youtube_category_extraction(text):
    try:

        cl_model = get_model()
        predictions_youtube, raw_outputs_youtube = cl_model.predict([text])
        return [list(youtube_categories_json)[predictions_youtube[0]]]

    except Exception as e:
        print(e)
        return ['Others']


def detect_ner(text):
    # Load the spaCy English language model
    nlp = spacy.load('en_core_web_sm')

    # Process the text with the model to generate a Doc object
    doc = nlp(text)

    # Extract named entities from the Doc object
    entities = []
    ignored_entities = ['CARDINAL']

    for ent in doc.ents:
        if ent.label_ not in ignored_entities:
            entities.append((ent.text, ent.label_))

    return entities

def extract_keywords(text):
    # Initialize the KeyBERT model with the 'distilbert-base-nli-mean-tokens' pre-trained model
    model = KeyBERT('distilbert-base-nli-mean-tokens')


    ignore_keywords = ['video', 'videos', 'love', 'loves', 'like', 'likes', '[', ']', 'good', 'new', 'bro']
    # Extract keywords with the model
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=5)
    # keywords = model.extract_keywords(text, top_n=5)
    keywords_out = []

    for keyword in keywords:
        try:
            if keyword[0] not in ignore_keywords:
                keywords_out.append(keyword[0])
        except Exception as e:
            print(e)

    return keywords_out

def sentiment_analysis_twitter_roberta_base_sentiment(input_text):

    sentiment_value = 'Neutral'

    if len(input_text) > 300:
        input_text = input_text[0:300]
    try:
        sentiment_list = sentiment_pipeline([input_text])
        print(colored(sentiment_list, 'green'))
        if (len(sentiment_list) == 1 and 'label' in sentiment_list[0]):
            if (sentiment_list[0]['label'] == 'LABEL_0'):
                return 'Negative'
            elif (sentiment_list[0]['label'] == 'LABEL_1'):
                return 'Neutral'
            elif (sentiment_list[0]['label'] == 'LABEL_2'):
                return 'Positive'
    except Exception as e:
        print(e)

    return sentiment_value

##########################################################



@application.route('/CA_single',methods=['GET','POST'])
def start_CA_single():

    request_type = flask.request.args.get('request_type', default='', type=str)
    text = flask.request.args.get('text', default='', type=str)


    if (request_type =='' or request_type == None):
        print('Invalid request_type !!!')
        json_out = {}
        json_out['query'] = text
        if (request_type == 'Sentiment Analysis'):
            json_out['result'] = 'Neutral'
        else:
            json_out['result'] = ['Others']

        return json_out

    if (text =='' or text == None):
        print('Invalid text !!!')
        json_out = {}
        json_out['query'] = text
        if (request_type == 'Sentiment Analysis'):
            json_out['result'] = 'Neutral'
        else:
            json_out['result'] = ['Others']

        return json_out


    json_out = {}
    json_out['query'] = text
    
   
    if (request_type == 'Youtube-Category Extraction'):
        category_result = youtube_category_extraction(text)
        json_out['result'] = category_result

    if (request_type == 'Named-Entity Recognition'):
        ner_result = detect_ner(text)
        json_out['result'] = ner_result
    
    if (request_type == 'Keyword Extraction'):
        ner_result = extract_keywords(text)
        json_out['result'] = ner_result

    if (request_type == 'Sentiment Analysis'):
        sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment(text)
        json_out['result'] = sentiment_result


    return json_out




if __name__ == "__main__":
    application.run(host='0.0.0.0')
