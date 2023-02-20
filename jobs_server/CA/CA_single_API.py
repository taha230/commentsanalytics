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


sentiment = SentimentIntensityAnalyzer()

application = flask.Flask(__name__)

application.config["DEBUG"] = True

##########################################################

def get_sentiment_result (input_text):
    return 'Neutral'

def sentiment_analysis_vader(input_text):

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

##########################################################



@application.route('/CA_single',methods=['GET','POST'])
def start_CA_single():

    request_type = flask.request.args.get('request_type', default='', type=str)
    text = flask.request.args.get('text', default='', type=str)


    if (request_type =='' or request_type == None):
        print('Invalid request_type !!!')
        json_out = {}
        json_out['query'] = text
        json_out['result'] = 'Neutral'
        return json_out

    if (text =='' or text == None):
        print('Invalid text !!!')
        json_out = {}
        json_out['query'] = text
        json_out['result'] = 'Neutral'
        return json_out


    json_out = {}
    json_out['query'] = text

    sentiment_result = 'Neutral'

    if (request_type == 'Sentiment Analysis'):
        sentiment_result = sentiment_analysis_vader(text)
        json_out['result'] = sentiment_result

   
    return json_out

if __name__ == "__main__":
    application.run(host='0.0.0.0')
