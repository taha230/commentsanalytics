from termcolor import colored
from SB.social_network_finder import cuf_tor, linkedin_tor
from SB.social_network_finder import maps_tor
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
import datetime
from bson.objectid import ObjectId




#################################### Variables ##############################################

PASSED_DAYS = 7

mongo_address = 'localhost'
DB_NAME = 'Profile_Browse'
COLLECTION_NAME_User_Log= 'User_Log'
client = MongoClient(mongo_address, 27017)
db = client[DB_NAME]
collection_User_Log = db[COLLECTION_NAME_User_Log]

#############################################################################################


def open_sqlite_db():
    while True:
        try:
            sqliteConnection = sqlite3.connect('../db.sqlite3')
            print("Successfully Connected to SQLite")
            return sqliteConnection

        except Exception as e:
            print(e)
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
            continue


def diff_day(d1, d2):
    return (d1.year - d2.year) * 365 + (d1.month - d2.month) * 30 + (d1.day - d2.day)


def get_passed_log_list(cursor):

    try:

        delete_list = []

        sqlite_select_query = """SELECT * from home_user_log """
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            diff_day_value = diff_day(datetime.datetime.now(), datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S.%f'))
            if (diff_day_value > PASSED_DAYS):
                delete_list.append(record)


        return delete_list



    except Exception as e:
        print(e)
        return []

def get_passed_log_list_mongodb():

    try:

        delete_list = []

        query_log= {}
        records = collection_User_Log.find(query_log)

        for record in records:
            diff_day_value = diff_day(datetime.datetime.now(), record['time_slot'])
            if (diff_day_value >= PASSED_DAYS):
                delete_list.append(record)


        return delete_list



    except Exception as e:
        print(e)
        return []

def clear_home_user_log_records(cursor,conn, log_id):

    while True:
        try:

            sqlite_delete_query = """
            DELETE FROM home_user_log WHERE id=?
            """

            cursor.execute(sqlite_delete_query, (log_id,))
            conn.commit()
            return

        except Exception as e:
            print(e)

def clear_home_user_log_records_mongodb(log_id):

    while True:
        try:

            collection_User_Log.delete_one({'_id': ObjectId(log_id)})
            return

        except Exception as e:
            print(e)

def delete_user_log ():

    conn = open_sqlite_db()
    cursor = conn.cursor()

    records_passed_log = get_passed_log_list(cursor)

    passed_count = 0
    if (len(records_passed_log) > 0):
        for log in records_passed_log:
            passed_count += 1
            log_id = log[0]
            clear_home_user_log_records(cursor,conn, log_id)

            print(colored(f' delete count { passed_count} / {len(records_passed_log)}', 'green'))


    cursor.close()
    close_sqlite_db(conn)


def delete_user_log_mongodb ():

    records_passed_log = get_passed_log_list_mongodb()

    passed_count = 0
    if (len(records_passed_log) > 0):
        for log in records_passed_log:
            passed_count += 1
            log_id = str(log['_id'])
            clear_home_user_log_records_mongodb(log_id)

            print(colored(f' delete count { passed_count} / {len(records_passed_log)}', 'green'))


   
################################################################################

while True:
    # delete_user_log()
    delete_user_log_mongodb()
    break

# update_passed_count()

