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
# from oauth2client.service_account import ServiceAccountCredentials
# from sshtunnel import SSHTunnelForwarder
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# no change_proxy

application = flask.Flask(__name__)

application.config["DEBUG"] = True



class Search_Engine(Enum):

    GOOGLE = 1
    DUCKDUCKGO = 2
    BING = 3
    YAHOO = 4
    ASK = 5
    YANDEX = 6


# def change_proxy():
#     '''
#     function_name: change_proxy
#     input: none
#     output: none
#     description: change proxy with proxyrotator api
#     '''
#     while True:
#         try:
#             url = 'http://falcon.proxyrotator.com:51337/'
#
#             params = dict(
#                 apiKey='HTpjCRPkV3sZyY5JS9tNbFKDgnzfqeAB',
#                 # port = 80,
#                 connectionType='Residential',
#                 country='US'
#                 # connectionType='Datacenter'
#             )
#
#             # print('********************************************')
#             data = ''
#
#
#
#             resp = requests.get(url=url, params=params)
#             data = json.loads(resp.text)
#
#             # print('Changing Proxy ... ' + data['proxy'])
#             # print('********************************************')
#
#             return data['proxy'], data['randomUserAgent']
#         except Exception as e:
#             print(e)
#             print('Error in changing proxy...')
#             continue
#
def change_proxy_bank():

    while True:
        try:
            client = MongoClient('localhost', 27017)
            db = client['proxy_bank_collection']
            collection = db['bank']

            current_time = datetime.datetime.now()
            time_past = (current_time - datetime.timedelta(minutes=int(1)))
            query = {"time_slot": {"$gte": time_past}}

            current_count = collection.find(query).count()
            if (current_count > 0):


                shuffle_index =  int(random.random() * (current_count-1))
                most_new_row = collection.find(query).sort([("time_slot", -1)])[shuffle_index] # get proxy shuffle
                # most_new_row = collection.find().sort([("time_slot", -1)])[0] # get proxy shuffle
                # collection.delete_one(most_new_row)
                client.close()
                print(colored('get proxy from Proxy Bank index : ' + str(shuffle_index) +' !!! (count : '+ str(current_count)+ ')'))
                return most_new_row['proxy'], most_new_row['useragent']

            else:
                print(colored('Waiting for filling Proxy Bank','magenta'))
                continue



        except Exception as e:
            print(e)


def change_proxy_consumer(website, db_producer):


    while True:

        try:
            collection_producer = None

            if (website == Search_Engine.GOOGLE):
                collection_producer = db_producer['google']
            if (website == Search_Engine.DUCKDUCKGO):
                collection_producer = db_producer['duckduckgo']
            if (website == Search_Engine.BING):
                collection_producer = db_producer['bing']
            if (website == Search_Engine.YAHOO):
                collection_producer = db_producer['yahoo']
            if (website == Search_Engine.ASK):
                collection_producer = db_producer['ask']
            if (website == Search_Engine.YANDEX):
                collection_producer = db_producer['yandex']

            collection_count = collection_producer.count()
            # collection_producer.create_index([("time_slot", 1)])


            if (collection_count == 0):
                print (colored('get new session !','yellow'))
                proxy1, useragent1 = change_proxy_bank()
                return True, proxy1, '',requests.session(), None

            else:
                most_new_row = collection_producer.find().sort([("time_slot", -1)])[0]
                collection_producer.delete_one(most_new_row)

                time_interval = (datetime.datetime.now() - most_new_row["time_slot"]).seconds / 60
                # print(colored('time to session: ' +str(time_interval) + ' min', 'green'))


                proxy1 = most_new_row['proxy1']

                session = pickle.loads(most_new_row['session'])
                # useragent1 = most_new_row['useragent']
                # cookie = pickle.loads(most_new_row['cookies'])


                # os.environ['http_proxy'] = proxy1
                # os.environ['HTTP_PROXY'] = proxy1
                # os.environ['https_proxy'] = proxy1
                # os.environ['HTTPS_PROXY'] = proxy1

                print (colored('get from producer (size_' + website.name + ' : '+ str(collection_count) +' )) !','yellow'))
                return True, proxy1, '', session, None

        except Exception as e:
            print (e)
            # os.system('sudo service mongod start')
            print('restart mongodb called !')
            # time.sleep(10)

            continue



##########################################################

def check_request(input_ip):

    valid_ip_list = [ \
                       '107.23.255.128','107.23.255.129','107.23.255.131','107.23.255.132','107.23.255.133','107.23.255.134', \
                       '107.23.255.135','107.23.255.137','107.23.255.138','107.23.255.139','107.23.255.140','107.23.255.141', \
                       '107.23.255.142','107.23.255.143','107.23.255.144','107.23.255.145','107.23.255.146','107.23.255.147', \
                       '107.23.255.148','107.23.255.149','107.23.255.150','107.23.255.151','107.23.255.152','107.23.255.153', \
                       '107.23.255.154','107.23.255.155','107.23.255.156','107.23.255.157','107.23.255.158','107.23.255.159', \
                       \
                       '35.162.152.183','52.38.28.241','52.35.67.149','54.149.215.237', \
                       \
                       '13.127.146.34','13.127.207.241','13.232.235.243','13.233.81.143', \
                       \
                       '13.112.233.15','54.250.57.56','18.182.156.77','52.194.200.157', \
                       \
                       '3.120.160.95','18.184.214.33','18.197.117.10','3.121.144.151', \
                       \
                       '13.239.156.114','13.238.1.253','13.54.58.4','54.153.234.158', \
                       \
                       '18.228.167.221', '18.228.209.157', '18.228.209.53', '18.228.69.72', \
                       \
                       '13.228.169.5', '3.0.35.31', '3.1.111.112', '52.220.50.179', \
                       \
                       '34.250.225.89', '52.30.208.221', '63.34.177.151', '63.35.2.11', \
                       \
                       '188.40.2.5', '151.238.66.86', '151.238.178.64', '127.0.0.1', \
                       '31.59.177.34', '31.59.188.175' \
        ]

    if input_ip not in valid_ip_list :
        return False
    else:
        return True

def read_google_spreadsheets (google_spreadsheets_url, column_name, sheet_name):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('goole-search-upwork-d86fb84fd7f1.json', scope)
    gc = gspread.authorize(creds)

    sheet1 = gc.open_by_url(google_spreadsheets_url).sheet1
    all_data = sheet1.get_all_records()

    column_row_list = []
    for data in all_data:
        if (column_name in data and data[column_name] != ''):
            column_row_list.append(data[column_name])
    print (colored('get form url : '+ google_spreadsheets_url +' and column-name : ' + str(column_name) +' with ' + str(len(column_row_list)) + ' row(s)', 'green'))
    return flask.jsonify(column_row_list)

############################### Global Variables #######################################################

process_num = 1
time_out = 10

producer_ip = 'localhost'
# producer_ip = '192.168.3.238'






@application.route('/google-sheet',methods=['GET','POST'])
def start():


    google_spreadsheets_url = flask.request.args.get('google_spreadsheets_url', default = '', type=str)
    column_name = flask.request.args.get('column_name', default = '', type=str)
    sheet_name = flask.request.args.get('sheet_name', default = 'sheet1', type=str)

    if (google_spreadsheets_url =='' or google_spreadsheets_url == None):
        return 'Invalid google_spreadsheets_url (url = '+ str(google_spreadsheets_url)  +' and column_name = ' + column_name +' ) !!!'
    # if (not check_request(ip_add_remote)):
    #     return 'Invalid IP !!! (' + str(ip_add_remote) + ')'

    return read_google_spreadsheets(google_spreadsheets_url, column_name, sheet_name)

if __name__ == "__main__":
    # application.run(host='0.0.0.0', Threaded = True)
    application.run(host='0.0.0.0')
