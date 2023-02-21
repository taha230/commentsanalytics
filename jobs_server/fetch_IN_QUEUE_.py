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
import mysql.connector
import datetime
import json
import sqlite3
import uuid
from bson.objectid import ObjectId



#################################### Variables ##############################################

sleep_time = 10

# ip_server = '176.9.22.248'
# ip_server = '138.201.111.134'
ip_server= '95.217.33.222'

port_insert = '8933'
port_delete = '8933'

mongo_address = 'localhost'
DB_NAME = 'CommentsAnalytics'
COLLECTION_NAME_BULKS = 'Bulks'
COLLECTION_NAME_REQUESTS = 'Requests'
client = MongoClient(mongo_address, 27017)
db = client[DB_NAME]
collection_Bulks = db[COLLECTION_NAME_BULKS]
collection_Requests = db[COLLECTION_NAME_REQUESTS]

##############################################################################################



def open_sqlite_db():
    while True:
        try:
            sqliteConnection = sqlite3.connect('../db.sqlite3')
            print("Successfully Connected to SQLite")
            return sqliteConnection

        except Exception as e:
            print(e)
            time.sleep(2)
            continue

def close_sqlite_db(conn):
    while True:
        try:
            if conn:
                conn.close()
                print("The SQLite connection is closed")
                return

        except Exception as e:
            print(e)
            time.sleep(2)
            continue

def get_in_queue_and_In_progress_list(cursor):

    try:

        sqlite_select_query = """SELECT * from home_bulk WHERE status = ? ORDER BY bulk_start_time_slot DESC"""
        cursor.execute(sqlite_select_query, ('In Queue',))
        records_In_Queue = cursor.fetchall()

        cursor.execute(sqlite_select_query, ('In Progress',))
        records_In_Progress = cursor.fetchall()

        return records_In_Queue, records_In_Progress



    except Exception as e:
        print(e)
        return [], []

def update_bulk_status(cursor, conn, bulk_id, status):

    while True:
        try:

            sqlite_update_query = """
            UPDATE home_bulk
            SET status = ?
            WHERE id = ?
            """

            cursor.execute(sqlite_update_query, (status, bulk_id))
            conn.commit()
            return

        except Exception as e:
            print(e)

def update_bulk_status_mongodb(bulk_id, status):

    while True:
        try:

            collection_Bulks.find_and_modify(query={'_id': ObjectId(bulk_id)}, update={'$set': {"status": status}})
            return

        except Exception as e:
            print(e)

def get_request_list_from_bulk(cursor, bulk_id):
    try:

        sqlite_select_query = """SELECT * from home_request WHERE bulk_id = ?"""
        cursor.execute(sqlite_select_query, (bulk_id,))
        records_bulk_requests = cursor.fetchall()

        return records_bulk_requests



    except Exception as e:
        print(e)
        return []

def get_request_list_from_bulk_mongodb(bulk_id):
    while True:
        try:
            query_bulk_id = {'bulk' : bulk_id}
            records_requests = collection_Requests.find(query_bulk_id)
            return records_requests
            
        except Exception as e:
            print(e)
            return []

def insert_new_Request_Bulk_Process(cursor, conn , request_id, query, request_type):
    try:

        sqlite_insert_query = """INSERT INTO home_request_bulk_process (id, process_status, request_id, query, request_type)
                                 VALUES (?, 'False' , ?, ?, ?)"""
        cursor.execute(sqlite_insert_query, (request_id, request_id, query, request_type))
        conn.commit()

        return

    except Exception as e:
        print(e)
        return

def insert_new_Request_Bulk_API(bulk_id, request_id, query, request_type):

    while True:
        try:

            url = "http://" + ip_server + ":" + port_insert + "/insert_request_bulk?bulk_id=" + str(bulk_id) + "&request_id=" + str(request_id) + "&request_type=" + str(request_type) + "&query=" + str(query)

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            if response.status_code == 200 :
                if (response.text == 'Exception occured!'):
                    continue
                elif response.text == 'query inserted to db!':
                    return response.text


        except Exception as e:
            print(e)
            continue


def run_fetch_in_queue ():

    try:
        conn = open_sqlite_db()
        cursor = conn.cursor()

        records_In_Queue, records_In_Progress = get_in_queue_and_In_progress_list(cursor)


        if (len(records_In_Progress) == 0 and len(records_In_Queue) > 0):
            oldest_in_queue_record = records_In_Queue[-1]
            bulk_id = oldest_in_queue_record[0]
            bulk_total_count = oldest_in_queue_record[5]

            # update bulk_status to 'In Progress'
            update_bulk_status (cursor, conn, bulk_id, 'In Progress')
            
            # insert to Request_Bulk_Process Table
            reqeusts_list = get_request_list_from_bulk(cursor, bulk_id)
            print (len(reqeusts_list))
            print(bulk_total_count)
            while len(reqeusts_list) != bulk_total_count:
                reqeusts_list = get_request_list_from_bulk(cursor, bulk_id)
                time.sleep(2)

            print(colored(str(len(reqeusts_list)), 'magenta'))

            counter_add = 0
            for request in reqeusts_list:
                counter_add += 1
                while True:
                    try:
                        query = request[4]
                        request_type = request[10]
                        request_id = request[0]
                        # insert_new_Request_Bulk_Process(cursor, conn, request_id, query, request_type)
                        insert_out = insert_new_Request_Bulk_API(bulk_id, request_id, query, request_type)
                        if insert_out == 'query inserted to db!':
                            break
                    except Exception as e:
                        print(e)
                        continue
            print(colored(f' {counter_add} inserted to Request_Bulk_Process!', 'green'))



        cursor.close()
        close_sqlite_db(conn)
    
    except Exception as e:
        print(e)

def run_fetch_in_queue_mongodb ():

    try:
        
        query_bulk_in_progress = {'status' : 'In Progress'}
        query_bulk_in_queue = {'status' : 'In Queue'}
        records_In_Progress = collection_Bulks.find(query_bulk_in_progress).sort([("bulk_start_time_slot", 1)])
        records_In_Queue = collection_Bulks.find(query_bulk_in_queue).sort([("bulk_start_time_slot", 1)])


        if (records_In_Progress.count() == 0 and records_In_Queue.count() > 0):
            oldest_in_queue_record = records_In_Queue[0]
            bulk_id = str(oldest_in_queue_record['_id'])
            bulk_total_count = oldest_in_queue_record['total_count']

            # update bulk_status to 'In Progress'
            update_bulk_status_mongodb (bulk_id, 'In Progress')
            
            # insert to Request_Bulk_Process Table
            reqeusts_list = get_request_list_from_bulk_mongodb(bulk_id)
            print (colored(reqeusts_list.count(), 'green'))
            print(colored(bulk_total_count, 'red'))
            while reqeusts_list.count() != bulk_total_count:
                reqeusts_list = get_request_list_from_bulk_mongodb(bulk_id)
                time.sleep(2)

            print(colored(str(reqeusts_list.count()), 'magenta'))

            counter_add = 0
            for request in reqeusts_list:
                counter_add += 1
                while True:
                    try:
                        query = request['query']
                        request_type = request['request_type']
                        request_id = str(request['_id'])
                        # insert_new_Request_Bulk_Process(cursor, conn, request_id, query, request_type)
                        insert_out = insert_new_Request_Bulk_API(bulk_id, request_id, query, request_type)
                        if insert_out == 'query inserted to db!':
                            break
                    except Exception as e:
                        print(e)
                        continue
            print(colored(f' {counter_add} inserted to Request_Bulk_Process!', 'green'))
            
    
    except Exception as e:
        print(e)

################################################################################

while True:
    # run_fetch_in_queue()
    run_fetch_in_queue_mongodb()
    print(colored('wait for ' + str(sleep_time) + ' seconds !!!', 'yellow'))
    time.sleep(sleep_time)
    

# run_fetch_in_queue()

