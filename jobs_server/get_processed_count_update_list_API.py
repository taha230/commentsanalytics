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
from bson.objectid import ObjectId


application = flask.Flask(__name__)

application.config["DEBUG"] = True



##########################################################

def get_update_json(bulk_id):

    try:
        client = MongoClient('localhost', 27017)
        db = client['CommentsAnalytics']
        collection = db['Requests']

        processed_count = collection.find({'bulk_id': bulk_id, 'status': True}).count()
        update_list = []


        find_cursor = collection.find({'bulk_id': bulk_id, 'status': True, 'update': False})

        for item in find_cursor:
            try:
                item_update = collection.find_and_modify(query={'_id': ObjectId(item['_id'])}, update={'$set': {"update": False}})

                update_json = {}
                update_json['bulk_id'] = item_update['bulk_id']
                update_json['request_id'] = item_update['request_id']
                update_json['result'] = item_update['result']
                update_json['time_slot'] = item_update['time_slot']
                update_json['request_type'] = item_update['request_type']
                update_json['query'] = item_update['query']
                if ('result_sentiment' in update_json):
                    update_json['result_sentiment'] = item_update['result_sentiment']

                update_list.append(update_json)

                # update the update flag

            except Exception as e:
                print(e)
                continue



        client.close()

        print (colored('number of processed for bulk_id ' + str(bulk_id) + ' >>  ' + str(processed_count),'green'))
        print (colored('number of update list for bulk_id ' + str(bulk_id) + ' >>  ' + str(len(update_list)),'blue'))

        out_json = {'processed_count' : processed_count , 'update_list' : update_list}
        return out_json


    except Exception as e:
        print (colored(str(e),'red'))
        return {'processed_count' : 0 , 'update_list' : []}


@application.route('/get_processed_count_update_list',methods=['GET','POST'])
def start_get_update():

    bulk_id = flask.request.args.get('bulk_id', default='', type=str)

    return flask.jsonify(get_update_json(bulk_id))



if __name__ == "__main__":
    application.run(host='0.0.0.0')
