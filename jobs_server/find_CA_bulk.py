from termcolor import colored
import requests
from bson.objectid import ObjectId
import pandas as pd
from pymongo import MongoClient
from torpy.http.requests import tor_requests_session
from multiprocessing import Manager
import multiprocessing
from torpy.http.urlopener import do_request as urllib_request
from torpy import TorClient
from torpy.http.adapter import TorHttpAdapter
import csv
from io import BytesIO
from base64 import b64decode
import base64
import urllib
import xlsxwriter
import time
import random
import sqlite3
import uuid
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import spacy
from keybert import KeyBERT

# sentiment_pipeline = pipeline("sentiment-analysis")
# sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
# sentiment_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")



#################################### Variables ##############################################
DB_NAME = 'Bulk_TOR'
COLLECTION_NAME = 'Query_CUF'

DB_NAME_REQUESTS = 'CommentsAnalytics'
COLLECTION_NAME_REQUESTS = 'Requests'

COLLECTION_CUF = 'CUF'
COLLECTION_Linkedin = 'Linkedin'

CUF_WEBSITE_FIELD_NAME = 'result'
sleep_time = 10
# IP_SINGLE_API = '95.217.33.222'
IP_SINGLE_API = '138.201.111.134'
IP_SINGLE_API_CATEGORY = '167.235.207.111' #'136.243.77.239' # '167.235.207.111'

##############################################################################################


#no change_proxy
mongo_address = 'localhost'
# mongo_address = '192.168.1.64'
client = MongoClient(mongo_address, 27017)
db = client[DB_NAME]
db_Requests = client[DB_NAME_REQUESTS]
collection = db[COLLECTION_NAME]
collection_Requests = db_Requests[COLLECTION_NAME_REQUESTS]
collection_CUF = db[COLLECTION_CUF]
collection_Linkedin = db[COLLECTION_Linkedin]

manager = Manager()
counter = manager.list()


def get_from_mongo():
    random_sleep_time = random.random()
    time.sleep(random_sleep_time)

    false_count = collection_Requests.find({'status': False}).count()
    if (false_count == 0):
        category = collection_Requests.find_and_modify(query={'status': 'process'}, update={'$set': {"status": 'process'}})
    else:
        category = collection_Requests.find_and_modify(query={'status': False}, update={'$set': {"status": 'process'}})
    return category

def update_mongo_sentiment(id, result):
    collection_Requests.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"status": True, 'result': result}})

def update_mongo_result_sentiment(id, result, result_sentiment):
    collection_Requests.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"status": True, 'result': result, 'result_sentiment': result_sentiment}})

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

def sentiment_analysis_twitter_roberta_base_sentiment_API(input_text):

    sentiment_value = 'Neutral'
    try:
        request_type = 'Sentiment Analysis'
        url = "http://" + str(IP_SINGLE_API_CATEGORY) + ":8943/CA_single?request_type=" + request_type +"&text=" + input_text

        payload = ""
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        if ('result' in response.json()):
            return response.json()['result']
    except Exception as e:
        print(e)

    return sentiment_value

def detect_ner(input_text):
    
    entities = []

    try:
        request_type = 'Named-Entity Recognition'
        url = "http://" + str(IP_SINGLE_API_CATEGORY) + ":8943/CA_single?request_type=" + request_type +"&text=" + input_text

        payload = ""
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        if ('result' in response.json()):
            return response.json()['result']
    except Exception as e:
        print(e)

    
    return entities

def extract_keywords(input_text):
    keywords_out = []

    try:
        request_type = 'Keyword Extraction'
        url = "http://" + str(IP_SINGLE_API_CATEGORY) + ":8943/CA_single?request_type=" + request_type +"&text=" + input_text

        payload = ""
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        if ('result' in response.json()):
            return response.json()['result']
    except Exception as e:
        print(e)

    
    return keywords_out

def extract_category_youtube(input_text):

    category_list = ['Others']

    try:
        request_type = 'Youtube-Category Extraction'
        url = "http://" + str(IP_SINGLE_API_CATEGORY) + ":8943/CA_single?request_type=" + request_type +"&text=" + input_text

        payload = ""
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        if ('result' in response.json()):
            return response.json()['result']
    except Exception as e:
        print(e)

    return category_list

def find_CA(index):

    item = get_from_mongo()

    while True:

        false_count = get_false_count()
        progress_count = get_process_count()

        print(colored(item, 'blue'))

        if item is None or (false_count == 0 and progress_count == 0):
            break
        try:

            if (len(item['query']) <= 2 and request_type == 'Sentiment Analysis' ):

                print(item['query'])
                update_mongo_sentiment(item['_id'], 'Neutral')

                counter.append('ok')
                print(colored(f'{len(counter)} === sentiment added to mongo', 'green'))

                item = get_from_mongo()

                if item is None:
                    break
            
            if (len(item['query']) <= 2 and request_type == 'Named-Entity Recognition' ):

                print(item['query'])
                update_mongo_result_sentiment(item['_id'], str([]), 'Neutral')

                counter.append('ok')
                print(colored(f'{len(counter)} === NER added to mongo', 'green'))

                item = get_from_mongo()

                if item is None:
                    break

            if (len(item['query']) <= 2 and request_type == 'Keyword Extraction' ):

                print(item['query'])
                update_mongo_result_sentiment(item['_id'], str([]), 'Neutral')

                counter.append('ok')
                print(colored(f'{len(counter)} === Keyword added to mongo', 'green'))

                item = get_from_mongo()

                if item is None:
                    break
            
            if (len(item['query']) <= 2 and request_type == 'Youtube-Category Extraction'):

                print(item['query'])
                update_mongo_result_sentiment(item['_id'], str([]), 'Neutral')

                counter.append('ok')
                print(colored(f'{len(counter)} === Keyword added to mongo', 'green'))

                item = get_from_mongo()

                if item is None:
                    break
        
            

            cname = item['query']
            request_type = item['request_type']

            result = ''           

            print(cname)

            if (request_type == 'Sentiment Analysis'):
                sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment_API(cname)
                result = sentiment_result
                update_mongo_sentiment(item['_id'], result)

            if (request_type == 'Named-Entity Recognition'):
                ner_result = detect_ner(cname)
                sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment_API(cname)
                update_mongo_result_sentiment(item['_id'], ner_result, sentiment_result)

            if (request_type == 'Keyword Extraction'):
                keyword_result = extract_keywords(cname)
                sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment_API(cname)
                update_mongo_result_sentiment(item['_id'], keyword_result, sentiment_result)
            
            if (request_type == 'Youtube-Category Extraction'):
                category_result = extract_category_youtube(cname)
                sentiment_result = sentiment_analysis_twitter_roberta_base_sentiment_API(cname)
                update_mongo_result_sentiment(item['_id'], category_result, sentiment_result)


            
           
            counter.append('ok')
            print(colored(f'{len(counter)} === company website added to mongo', 'green'))

            item = get_from_mongo()

            if item is None:
                break

        except Exception as e:
            print(e)
            pass



def run_():
    number_processes = 1


    processes = []

    for i in range(number_processes):
        # random_wait = random.random() * 3
        # time.sleep(random_wait)
        processes.append(multiprocessing.Process(target=find_CA, args=[i]))

    for p in processes:
        p.start()

    for p in processes:
        p.join()


################################################################################

def get_false_count():
    try:
        return collection_Requests.find({'status': False}).count()

    except Exception as e:
        print(e)
        return 10000

def get_process_count():
    try:
        return collection_Requests.find({'status': 'process'}).count()

    except Exception as e:
        print(e)
        return 10000



while True:

    false_count = get_false_count()
    process_count = get_process_count()

    print('false count : ' + str(false_count))
    print('processed count : ' + str(process_count))


    if (false_count !=0 or process_count != 0):
        run_()
    print(colored('wait for ' + str(sleep_time) + ' seconds !!!', 'yellow'))

    time.sleep(sleep_time)


