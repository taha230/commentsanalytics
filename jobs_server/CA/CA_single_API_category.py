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


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

model_path = "outputs/model_args.json"


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
    
    return json_out




if __name__ == "__main__":
    application.run(host='0.0.0.0')
