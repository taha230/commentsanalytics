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
import spacy
from keybert import KeyBERT

# sentiment_pipeline = pipeline("sentiment-analysis")
# sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
sentiment_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")


application = flask.Flask(__name__)

application.config["DEBUG"] = True

##########################################################

def get_sentiment_result (input_text):
    return 'Neutral'

def sentiment_analysis_vader(input_text):

    sentiment = SentimentIntensityAnalyzer()
    sentiment_value = 'Neutral'
    try:
        sentiment_json = sentiment.polarity_scores(input_text)
        # print(sentiment_json)
        if ('neg' in sentiment_json and 'neu' in sentiment_json and 'pos' in sentiment_json ):
            if (sentiment_json['neg'] > sentiment_json['neu'] and sentiment_json['neg'] > sentiment_json['pos']):
                sentiment_value = 'Negative'
            elif (sentiment_json['neu'] > sentiment_json['neg'] and sentiment_json['neu'] > sentiment_json['pos']):
                sentiment_value = 'Neutral'
            elif (sentiment_json['pos'] > sentiment_json['neg'] and sentiment_json['pos'] > sentiment_json['neu']):
                sentiment_value = 'Positive'
        else:
            print('no valid sentiment json')
    except Exception as e:
        print(e)

    return sentiment_value

def sentiment_analysis_twitter_roberta_base_sentiment(input_text):

    sentiment_value = 'Neutral'
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

    # Extract keywords with the model
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=3)
    # keywords = model.extract_keywords(text, top_n=5)
    keywords_out = [keyword[0] for keyword in keywords]

    return keywords_out

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
            json_out['result'] = str([])

        return json_out

    if (text =='' or text == None):
        print('Invalid text !!!')
        json_out = {}
        json_out['query'] = text
        if (request_type == 'Sentiment Analysis'):
            json_out['result'] = 'Neutral'
        else:
            json_out['result'] = str([])

        return json_out


    json_out = {}
    json_out['query'] = text

    sentiment_result = 'Neutral'

    if (request_type == 'Sentiment Analysis'):
        sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment(text)
        json_out['result'] = sentiment_result

    if (request_type == 'Named-Entity Recognition'):
        ner_result = detect_ner(text)
        json_out['result'] = ner_result
    
    if (request_type == 'Keyword Extraction'):
        ner_result = extract_keywords(text)
        json_out['result'] = ner_result
   
    return json_out




if __name__ == "__main__":
    application.run(host='0.0.0.0')
