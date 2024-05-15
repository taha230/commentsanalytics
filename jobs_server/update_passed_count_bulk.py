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



#################################### Variables ##############################################

sleep_time = 10

# ip_server = '176.9.22.248'
ip_server = '95.217.33.222' #'138.201.111.134'
# ip_server= '95.217.33.222'


port_get_update = '8934'

mongo_address = 'localhost'
DB_NAME = 'CommentsAnalytics'
COLLECTION_NAME_BULKS = 'Bulks'
COLLECTION_NAME_REQUESTS = 'Requests'
client = MongoClient(mongo_address, 27017)
db = client[DB_NAME]
collection_Bulks = db[COLLECTION_NAME_BULKS]
collection_Requests = db[COLLECTION_NAME_REQUESTS]

#############################################################################################


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

def update_bulk_end_time_slot(cursor, conn, bulk_id, time_slot):

    while True:
        try:

            sqlite_update_query = """
            UPDATE home_bulk
            SET bulk_end_time_slot = ?
            WHERE id = ?
            """

            cursor.execute(sqlite_update_query, (time_slot, bulk_id))
            conn.commit()
            return

        except Exception as e:
            print(e)


def update_bulk_end_time_slot_mongodb(bulk_id, time_slot):

    while True:
        try:

            collection_Bulks.find_and_modify(query={'_id': ObjectId(bulk_id)}, update={'$set': {"bulk_end_time_slot": time_slot}})
            return

        except Exception as e:
            print(e)


def clear_home_request_bulk_process_db_records(cursor,conn, bulk_id):

    while True:
        try:

            sqlite_update_query = """
            DELETE FROM home_request_bulk_process WHERE id=?
            """

            cursor.execute(sqlite_update_query, (time_slot, bulk_id))
            conn.commit()
            return

        except Exception as e:
            print(e)

def update_bulk_passed_count(cursor, conn, bulk_id, passed_count):

    while True:
        try:

            sqlite_update_query = """
            UPDATE home_bulk
            SET passed_count = ?
            WHERE id = ?
            """

            cursor.execute(sqlite_update_query, (passed_count, bulk_id))
            conn.commit()
            return

        except Exception as e:
            print(e)

def update_bulk_passed_count_mongodb(bulk_id, passed_count):

    while True:
        try:

            collection_Bulks.find_and_modify(query={'_id': ObjectId(bulk_id)}, update={'$set': {"passed_count": passed_count}})
            return

        except Exception as e:
            print(e)

def get_passed_count(cursor, bulk_id):

    try:
        sqlite_select_query = """SELECT * from home_request WHERE status = ? AND bulk_id= ?"""
        cursor.execute(sqlite_select_query, ('Success', bulk_id,))
        records_success = cursor.fetchall()
        return len(records_success)


    except Exception as e:
        print(e)
        return -1

def get_passed_count_API(bulk_id):

        try:

            url = "http://" + ip_server + ":" + port_get_update + "/get_processed_count_update_list?bulk_id=" + str(
                bulk_id)

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            if response.status_code == 200:
                if 'processed_count' in response.json() and 'update_list' in response.json():
                    return response.json()['processed_count'], response.json()['update_list']

            return -1 , []


        except Exception as e:
            print(e)
            return -1 , []


def update_request_sqlite(conn , cursor, id, url):

    while True:

        try:

            # update status and result in home_request
            sqlite_update_query_status_result = """
                                   UPDATE home_request
                                   SET status = ? , result = ? , result_time_slot = ? 
                                   WHERE id = ?
                                   """

            cursor.execute(sqlite_update_query_status_result, ('Success', url, datetime.datetime.now(), id))

            ###############################################################
            conn.commit()


            return

        except Exception as e:
            print(e)

def update_request_mongodb(id, url):

    while True:

        try:

            collection_Requests.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"status": 'Success', "result": url, "result_time_slot": datetime.datetime.now()}})
            return

        except Exception as e:
            print(e)

def update_request_sentiment_mongodb(id, sentiment):

    while True:

        try:

            collection_Requests.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"result_sentiment": sentiment}})
            return

        except Exception as e:
            print(e)


def update_passed_count ():

    conn = open_sqlite_db()
    cursor = conn.cursor()

    records_In_Queue, records_In_Progress = get_in_queue_and_In_progress_list(cursor)

    if (len(records_In_Progress) > 0):
        for in_progress_bulk in records_In_Progress:
            bulk_id = in_progress_bulk[0]
            total_count = in_progress_bulk[5]
            bulk_name = in_progress_bulk[3]

            print('bulk_id : ' + str(bulk_id))

            passed_count, update_list = get_passed_count_API(bulk_id)
            print('passed : ' + str(passed_count))
            print('count update list : ' + str(len(update_list)))

            # update bulk_status to 'In Progress'
            if (passed_count >= 0):
                update_bulk_passed_count (conn, cursor, bulk_id, passed_count)
                for update_request in update_list:
                    # update request fields in sqlite
                    if ('request_id' in update_request and 'result' in update_request):
                        update_request(conn, cursor, update_request['request_id'], update_request['result'])

            # update bulk_end_time_slot and status on complete level
            if (passed_count >= total_count):
                update_bulk_status(conn, cursor, bulk_id, 'Completed')
                update_bulk_end_time_slot (cursor, conn, bulk_id, datetime.datetime.now())
                # clear_home_request_bulk_process_db_records(cursor, conn, bulk_id)


            print(colored(f' passed count of bulk { bulk_name } update to  { passed_count}', 'green'))


    cursor.close()
    close_sqlite_db(conn)

def update_passed_count_mongodb():


    query_bulk_in_progress = {'status' : 'In Progress'}
    query_bulk_in_queue = {'status' : 'In Queue'}
    records_In_Progress = collection_Bulks.find(query_bulk_in_progress).sort([("bulk_start_time_slot", 1)])
    records_In_Queue = collection_Bulks.find(query_bulk_in_queue).sort([("bulk_start_time_slot", 1)])

    if (records_In_Progress.count() > 0):
        for in_progress_bulk in records_In_Progress:
            bulk_id = str(in_progress_bulk['_id'])
            total_count = in_progress_bulk['total_count']
            bulk_name = in_progress_bulk['name']

            print('bulk_id : ' + str(bulk_id))

            passed_count, update_list = get_passed_count_API(bulk_id)
            print('passed : ' + str(passed_count))
            print('count update list : ' + str(len(update_list)))

            # update bulk passed count
            if (passed_count >= 0):
                update_bulk_passed_count_mongodb (bulk_id, passed_count)
                for update_request in update_list:
                    print(update_request)
                    # update request fields in sqlite
                    if ('request_id' in update_request and 'result' in update_request):
                        update_request_mongodb(update_request['request_id'], update_request['result'])
                    if ('request_id' in update_request and 'result_sentiment' in update_request):
                        update_request_sentiment_mongodb(update_request['request_id'], update_request['result_sentiment'])

            # update bulk_end_time_slot and status on complete level
            if (passed_count >= total_count):
                update_bulk_status_mongodb(bulk_id, 'Completed')
                update_bulk_end_time_slot_mongodb (bulk_id, datetime.datetime.now())
                # clear_home_request_bulk_process_db_records(cursor, conn, bulk_id)


            print(colored(f' passed count of bulk { bulk_name } update to  { passed_count}', 'green'))


################################################################################

while True:
    # update_passed_count()
    update_passed_count_mongodb()
    print(colored('wait for '+ str(sleep_time) + ' seconds !!!', 'yellow'))
    time.sleep(sleep_time)

# update_passed_count()

