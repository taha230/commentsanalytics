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

application = flask.Flask(__name__)

application.config["DEBUG"] = True



##########################################################

def delete_db(bulk_id):

    try:
        client = MongoClient('localhost', 27017)
        db = client['CommentsAnalytics']
        collection = db['Requests']


        collection.remove({'bulk_id': bulk_id})
        client.close()

        print (colored('bulk deleted!','green'))

        return 'bulk deleted!'


    except Exception as e:
        print (colored(str(e),'red'))
        return 'Exception occured!'

def insert_db(query, request_type, bulk_id, request_id):

    try:
        client = MongoClient('localhost', 27017)
        db = client['CommentsAnalytics']
        collection = db['Requests']


        input_json ={'query': query, 'request_type': request_type, 'bulk_id': bulk_id, 'request_id': request_id, 'status': False, 'time_slot': datetime.datetime.now(), 'result': None, 'update': False}

        collection.insert_one(input_json)
        client.close()

        print (colored('query inserted to db!','green'))

        return 'query inserted to db!'


    except Exception as e:
        print (colored(str(e),'red'))
        return 'Exception occured!'

@application.route('/insert_request_bulk',methods=['GET','POST'])
def start_insert():

    bulk_id = flask.request.args.get('bulk_id', default='', type=str)
    request_id = flask.request.args.get('request_id', default='', type=str)
    request_type = flask.request.args.get('request_type', default='', type=str)
    query = flask.request.args.get('query', default='', type=str)

    return insert_db(query, request_type, bulk_id, request_id)


@application.route('/delete_requests_bulk',methods=['GET','POST'])
def start_delete():

    bulk_id = flask.request.args.get('bulk_id', default='', type=str)

    return delete_db(bulk_id)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
