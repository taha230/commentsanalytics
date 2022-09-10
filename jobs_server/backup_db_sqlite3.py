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
import shutil
from zipfile import ZipFile
import os
import glob
import bson




#################################### Variables ##############################################

BACKUP_DIR_SQLITE = '/home/archive_sqlite/'
BACKUP_DIR_MONGO = '/home/archive_mongo/'
PASSED_DAYS = 30


mongo_address = 'localhost'
DB_NAME = 'Profile_Browse'
COLLECTION_NAME_BULKS = 'Bulks'
COLLECTION_NAME_REQUESTS = 'Requests'
COLLECTION_NAME_User_Log= 'User_Log'

client = MongoClient(mongo_address, 27017)

#############################################################################################


def diff_day(d1, d2):
    return (d1.year - d2.year) * 365 + (d1.month - d2.month) * 30 + (d1.day - d2.day)

def dump(collections, conn, db_name, path):
    """
    MongoDB Dump
    :param collections: Database collections name
    :param conn: MongoDB client connection
    :param db_name: Database name
    :param path:
    :return:
    
    >>> DB_BACKUP_DIR = '/path/backups/'
    >>> conn = MongoClient("mongodb://admin:admin@127.0.0.1:27017", authSource="admin")
    >>> db_name = 'my_db'
    >>> collections = ['collection_name', 'collection_name1', 'collection_name2']
    >>> dump(collections, conn, db_name, DB_BACKUP_DIR)
    """

    db = conn[db_name]
    for coll in collections:
        timeStamp = datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")
        file_name = os.path.join(path, f'mongo_profilebrowse_{timeStamp}_{coll}.bson')
        with open(file_name, 'wb+') as f:
            for doc in db[coll].find():
                f.write(bson.BSON.encode(doc))

def backup_db_sqlite():
    try:
    
        timeStamp = datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")
        file_name = 'sqlite_profilebrowse_' + timeStamp + '.zip'
        file_path = BACKUP_DIR_SQLITE + file_name
        # create a ZipFile object

        zipObj = ZipFile(file_path, 'w')
        # Add multiple files to the zip
        zipObj.write('../db.sqlite3')

        # close the Zip File
        zipObj.close()
        return


    except Exception as e:
        print(e)

def backup_db_mongodb():
    try:
    
        collections = [COLLECTION_NAME_BULKS, COLLECTION_NAME_REQUESTS, COLLECTION_NAME_User_Log]
        dump(collections, client, DB_NAME, BACKUP_DIR_MONGO)
        return


    except Exception as e:
        print(e)

def delete_passed_archive():
    try:
    
        zip_list = glob.glob(BACKUP_DIR_SQLITE + "*.zip")
        for zip_file in zip_list:
            file_time_slot = datetime.datetime.strptime(zip_file.split('/')[-1].replace('.zip', '').replace('sqlite_profilebrowse_', ''), "%b-%d-%y-%H:%M:%S")
            diff_day_value = diff_day(datetime.datetime.now(), file_time_slot)
            if (diff_day_value > PASSED_DAYS):
                os.remove(zip_file)

        bson_list = glob.glob(BACKUP_DIR_MONGO + "*.bson")
        for bson_file in bson_list:
            file_time_slot = datetime.datetime.strptime(bson_file.split('/')[-1].replace('mongo_profilebrowse_', '').split('_')[0], "%b-%d-%y-%H:%M:%S")
            diff_day_value = diff_day(datetime.datetime.now(), file_time_slot)
            if (diff_day_value > PASSED_DAYS):
                os.remove(bson_file)

        


    except Exception as e:
        print(e)
################################################################################

while True:
    backup_db_sqlite()
    backup_db_mongodb()

    delete_passed_archive()
    break


