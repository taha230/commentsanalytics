from termcolor import colored
from SB.social_network_finder import cuf_tor, linkedin_tor, sb_tor
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
import random
import sqlite3
import uuid
import datetime



#################################### Variables ##############################################
DB_NAME = 'Bulk_TOR'
COLLECTION_NAME = 'Query_CUF'

DB_NAME_REQUESTS = 'Social_Browse'
COLLECTION_NAME_REQUESTS = 'Requests'

COLLECTION_CUF = 'CUF'
COLLECTION_Linkedin = 'Linkedin'

CUF_WEBSITE_FIELD_NAME = 'result'
sleep_time = 10
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


def get_from_mongo_total():
    return collection.find({})

def get_from_mongo_email():
    category = collection.find_and_modify(query={'email_tag': 'progress'}, update={'$set': {"email_tag": 'progressing'}})
    return category

def update_mongo_email(id, emails):
    collection.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"email_tag": True, 'company_emails': emails}})

def get_from_mongo_url():
    random_sleep_time = random.random()
    time.sleep(random_sleep_time)

    false_count = collection_Requests.find({'status': False}).count()
    if (false_count == 0):
        category = collection_Requests.find_and_modify(query={'status': 'process'}, update={'$set': {"status": 'process'}})
    else:
        category = collection_Requests.find_and_modify(query={'status': False}, update={'$set': {"status": 'process'}})
    return category

def get_from_mongo_not_found():
    category = collection.find_and_modify(query={'url_tag': False, 'company_website' : 'Not Found'}, update={'$set': {"url_tag": 'progress'}})
    return category

def update_mongo_url(id, url):
    collection_Requests.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"status": True, CUF_WEBSITE_FIELD_NAME: url}})

def update_mongo_google_maps(id, url):
    collection.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"url_tag": True, 'google_maps_website': url}})

def chunkIt(seq, num):
    '''
    function_name: chunkIt
    input: list, number of parts
    output: list of lists
    description: split list with approximate num of elements in each parts
    '''
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def calc_uule(input_address):
    encodedAddress = urllib.parse.quote(base64.b64encode(input_address.encode('ascii')))
    length_secret_json = {
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "j",
    10: "K",
    11:"L",
    12: "M",
    13: "N",
    14: "0",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
    26: "a",
    27: "b",
    28: "c",
    29: "d",
    30: "e",
    31: "f",
    32: "g",
    33: "h",
    34: "i",
    35: "j",
    36: "k",
    37: "l",
    38: "m",
    39: "n",
    40: "o",
    41: "p",
    42: "q",
    43: "r",
    44: "s",
    45: "t",
    46: "u",
    47: "v",
    48: "w",
    49: "x",
    50: "y",
    51: "z",
    52: 0,
    53: 1,
    54: 2,
    55: 3,
    56: 4,
    57: 5,
    58: 6,
    59: 7,
    60: 8,
    61: 9,
    62: "-",
    63: "",
    64: "A",
    65: "B",
    66: "C",
    67: "D",
    68: "E",
    69: "F",
    70: "G",
    71: "H",
    72: "I",
    73: "J",
    74: "K",
    75: "L",
    76: "M",
    77: "N",
    78: "O",
    79: "P",
    80: "Q",
    81: "R",
    82: "S",
    83: "T",
    89: "L"
}
    secretPart = length_secret_json[len(input_address)]
    uule = 'w+CAIQICI' + str(secretPart) + encodedAddress
    return uule

def check_mongodb_exist_CUF(companyName):

    companyName = companyName.lower()

    try:

        find_in_db_lower = collection_CUF.find_one({'company_name': companyName})

        if (find_in_db_lower == None):
            return None
        elif find_in_db_lower != None:

            return find_in_db_lower


    except Exception as e:
        print (colored(e,'red'))
        return None

def check_mongodb_exist_Linkedin(companyName):

    companyName = companyName.lower()

    try:

        find_in_db_lower = collection_Linkedin.find_one({'company_name': companyName})

        if (find_in_db_lower == None):
            return None
        elif find_in_db_lower != None:

            return find_in_db_lower


    except Exception as e:
        print (colored(e,'red'))
        return None

def check_mongodb_exist_social_network(companyName, social_network):

    companyName = companyName.lower()

    try:
        client_company_web = MongoClient('localhost', 27017)
        db_company_web = client_company_web['company_web_collection']

        collection_company_web = None
        if (social_network == 'Linkedin'):
            collection_company_web = db_company_web['company_linkedin']
        elif (social_network == 'Facebook'):
            collection_company_web = db_company_web['company_facebook']
        elif (social_network == 'Twitter'):
            collection_company_web = db_company_web['company_twitter']
        elif (social_network == 'Myspace'):
            collection_company_web = db_company_web['company_myspace']
        elif (social_network == 'Plaxo'):
            collection_company_web = db_company_web['company_plaxo']
        elif (social_network == 'Instagram'):
            collection_company_web = db_company_web['company_instagram']
        elif (social_network == 'Tumblr'):
            collection_company_web = db_company_web['company_tumblr']
        elif (social_network == 'Livejournal'):
            collection_company_web = db_company_web['company_livejournal']
        elif (social_network == 'Flickr'):
            collection_company_web = db_company_web['company_flickr']
        elif (social_network == 'Youtube'):
            collection_company_web = db_company_web['company_youtube']
        elif (social_network == 'Pinterest'):
            collection_company_web = db_company_web['company_pinterest']
        elif (social_network == 'Vimeo'):
            collection_company_web = db_company_web['company_vimeo']
        elif (social_network == 'Spotify'):
            collection_company_web = db_company_web['company_spotify']
        elif (social_network == 'Twitch'):
            collection_company_web = db_company_web['company_twitch']
        elif (social_network == 'Telegram'):
            collection_company_web = db_company_web['company_telegram']
        elif (social_network == 'WhatsApp'):
            collection_company_web = db_company_web['company_whatsapp']
        elif (social_network == 'WeChat'):
            collection_company_web = db_company_web['company_wechat']
        elif (social_network == 'TikTok'):
            collection_company_web = db_company_web['company_tiktok']
        elif (social_network == 'Snapchat'):
            collection_company_web = db_company_web['company_snapchat']
        elif (social_network == 'Reddit'):
            collection_company_web = db_company_web['company_reddit']
        elif (social_network == 'Website'):
            collection_company_web = db_company_web['company_website']
        elif (social_network == 'KnowledgePanel'):
            collection_company_web = db_company_web['company_knowledgepanel']
        elif (social_network == 'Wikipedia'):
            collection_company_web = db_company_web['company_wikipedia']
        elif (social_network == 'IMDb'):
            collection_company_web = db_company_web['company_imdb']
        elif (social_network == 'Booking'):
            collection_company_web = db_company_web['company_booking']
        elif (social_network == 'Github'):
            collection_company_web = db_company_web['company_github']
        elif (social_network == 'GoogleScholar'):
            collection_company_web = db_company_web['company_googlescholar']
        elif (social_network == 'Crunchbase'):
            collection_company_web = db_company_web['company_crunchbase']
        elif (social_network == 'Zoominfo'):
            collection_company_web = db_company_web['company_zoominfo']
        elif (social_network == 'StackOverflow'):
            collection_company_web = db_company_web['company_stackoverflow']
        elif (social_network == 'Amazon'):
            collection_company_web = db_company_web['company_amazon']

        find_in_db = collection_company_web.find_one({'company_name': companyName})
        client_company_web.close()

        if (find_in_db == None):
            return False
        else:
            return find_in_db

    except Exception as e:
        print(e)
        return False

def add_mongodb_CUF(query, website):

    query_lower = query.lower()

    try:
        updateJson ={'company_name': query_lower, 'url': website}

        find_record = collection_CUF.find_one({'company_name': query_lower})
        if (find_record == None and website != 'Not Found'):
            collection_CUF.insert_one(updateJson)
            print(colored('company name : ' + query_lower + ', website: ' + website +' added to CUF db!!! ', 'yellow'))

    except Exception as e:
        print(e)

def add_mongodb_Linkedin(query, website):

    query_lower = query.lower()

    try:

        updateJson ={'company_name': query_lower, 'url': website}

        find_record = collection_Linkedin.find_one({'company_name': query_lower})
        if (find_record == None and website != 'Not Found'):
            collection_Linkedin.insert_one(updateJson)
            print(colored('company name : ' + query_lower + ', website: ' + website +' added to Linkedin db!!! ', 'yellow'))


    except Exception as e:
        print(e)

def add_mongodb_social_network(companyName, selected_website, social_network):

    try:
        companyName = companyName.lower()
        client_company_web = MongoClient('localhost', 27017)
        db_company_web = client_company_web['company_web_collection']

        collection_company_web = None
        if (social_network == 'Linkedin'):
            collection_company_web = db_company_web['company_linkedin']
        elif (social_network == 'Facebook'):
            collection_company_web = db_company_web['company_facebook']
        elif (social_network == 'Twitter'):
            collection_company_web = db_company_web['company_twitter']
        elif (social_network == 'Myspace'):
            collection_company_web = db_company_web['company_myspace']
        elif (social_network == 'Plaxo'):
            collection_company_web = db_company_web['company_plaxo']
        elif (social_network == 'Instagram'):
            collection_company_web = db_company_web['company_instagram']
        elif (social_network == 'Tumblr'):
            collection_company_web = db_company_web['company_tumblr']
        elif (social_network == 'Livejournal'):
            collection_company_web = db_company_web['company_livejournal']
        elif (social_network == 'Flickr'):
            collection_company_web = db_company_web['company_flickr']
        elif (social_network == 'Youtube'):
            collection_company_web = db_company_web['company_youtube']
        elif (social_network == 'Pinterest'):
            collection_company_web = db_company_web['company_pinterest']
        elif (social_network == 'Vimeo'):
            collection_company_web = db_company_web['company_vimeo']
        elif (social_network == 'Spotify'):
            collection_company_web = db_company_web['company_spotify']
        elif (social_network == 'Twitch'):
            collection_company_web = db_company_web['company_twitch']
        elif (social_network == 'Telegram'):
            collection_company_web = db_company_web['company_telegram']
        elif (social_network == 'WhatsApp'):
            collection_company_web = db_company_web['company_whatsapp']
        elif (social_network == 'WeChat'):
            collection_company_web = db_company_web['company_wechat']
        elif (social_network == 'TikTok'):
            collection_company_web = db_company_web['company_tiktok']
        elif (social_network == 'Snapchat'):
            collection_company_web = db_company_web['company_snapchat']
        elif (social_network == 'Reddit'):
            collection_company_web = db_company_web['company_reddit']
        elif (social_network == 'Website'):
            collection_company_web = db_company_web['websites']
        elif (social_network == 'KnowledgePanel'):
            collection_company_web = db_company_web['company_knowledgepanel']
        elif (social_network == 'Wikipedia'):
            collection_company_web = db_company_web['company_wikipedia']
        elif (social_network == 'IMDb'):
            collection_company_web = db_company_web['company_imdb']
        elif (social_network == 'Github'):
            collection_company_web = db_company_web['company_github']
        elif (social_network == 'Booking'):
            collection_company_web = db_company_web['company_booking']
        elif (social_network == 'GoogleScholar'):
            collection_company_web = db_company_web['company_googlescholar']
        elif (social_network == 'Crunchbase'):
            collection_company_web = db_company_web['company_crunchbase']
        elif (social_network == 'Zoominfo'):
            collection_company_web = db_company_web['company_zoominfo']
        elif (social_network == 'StackOverflow'):
            collection_company_web = db_company_web['company_stackoverflow']
        elif (social_network == 'Amazon'):
            collection_company_web = db_company_web['company_amazon']

        updateJson ={'company_name': companyName, 'company_website': selected_website}
        collection_company_web.insert_one(updateJson)
        client_company_web.close()

    except Exception as e:
        print(e)

def find_sb(parts, index):

    item = get_from_mongo_url()

    while True:

        false_count = get_false_count()
        progress_count = get_process_count()



        if item is None or (false_count == 0 and progress_count == 0):
            break
        try:

            if (len(item['query']) <= 2 ):
                print(item['query'])
                update_mongo_url(item['_id'], 'not exists')

                counter.append('ok')
                print(colored(f'{len(counter)} === company website added to mongo', 'green'))

                item = get_from_mongo_url()

                if item is None:
                    break
                continue

            find_in_db = check_mongodb_exist_social_network(item['query'], item['request_type'])
            # find_in_db = False

            if (find_in_db and ('company_website' in find_in_db)):
                print(colored('company_name : ' + item['query'] + ' already exists in mongodb !', 'green'))
                print(item['query'])
                update_mongo_url(item['_id'], find_in_db['company_website'])

                counter.append('ok')
                print(colored(f'{len(counter)} === company website added to mongo', 'green'))

                item = get_from_mongo_url()

                if item is None:
                    break
                continue

            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            }

            with tor_requests_session() as s:
                s.headers.update(header)
                while True:
                    if item is None:
                        break

                    cname = item['query']

                    social_network = item['request_type']

                    # check db
                    find_in_db = False

                    # if (service == 'CUF'):
                    #     find_in_db = check_mongodb_exist_CUF(cname)




                    result = 'not exists'

                    query_website = ''

                    if (social_network == 'Twitter'):
                        query_website = 'twitter.com'
                    elif (social_network == 'Linkedin'):
                        query_website = 'linkedin.com'
                    elif (social_network == 'Facebook'):
                        query_website = 'facebook.com'
                    elif (social_network == 'Myspace'):
                        query_website = 'myspace.com'
                    elif (social_network == 'Plaxo'):
                        query_website = 'plaxo.com'
                    elif (social_network == 'Instagram'):
                        query_website = 'instagram.com'
                    elif (social_network == 'Tumblr'):
                        query_website = 'tumblr.com'
                    elif (social_network == 'Livejournal'):
                        query_website = 'livejournal.com'
                    elif (social_network == 'Flickr'):
                        query_website = 'flickr.com'
                    elif (social_network == 'Youtube'):
                        query_website = 'youtube.com'
                    elif (social_network == 'Pinterest'):
                        query_website = 'pinterest.com'
                    elif (social_network == 'Vimeo'):
                        query_website = 'vimeo.com'
                    elif (social_network == 'Spotify'):
                        query_website = 'spotify.com'
                    elif (social_network == 'Twitch'):
                        query_website = 'twitch.tv'
                    elif (social_network == 'Telegram'):
                        query_website = 't.me'
                    elif (social_network == 'WhatsApp'):
                        query_website = 'whatsapp.com'
                    elif (social_network == 'WeChat'):
                        query_website = 'wechat.com'
                    elif (social_network == 'TikTok'):
                        query_website = 'tiktok.com'
                    elif (social_network == 'Snapchat'):
                        query_website = 'snapchat.com'
                    elif (social_network == 'Reddit'):
                        query_website = 'reddit.com'
                    elif (social_network == 'Wikipedia'):
                        query_website = 'wikipedia.org'
                    elif (social_network == 'IMDb'):
                        query_website = 'imdb.com'
                    elif (social_network == 'Github'):
                        query_website = 'github.com'
                    elif (social_network == 'Booking'):
                        query_website = 'booking.com'
                    elif (social_network == 'GoogleScholar'):
                        query_website = 'scholar.google.com'
                    elif (social_network == 'Crunchbase'):
                        query_website = 'crunchbase.com/organization'
                    elif (social_network == 'Zoominfo'):
                        query_website = 'zoominfo.com/c'
                    elif (social_network == 'StackOverflow'):
                        query_website = 'stackoverflow.com/users'
                    elif (social_network == 'Amazon'):
                        query_website = 'amazon.com/stores'
                    else:
                        update_mongo_url(item['_id'], result)

                        counter.append('ok')
                        print(colored(f'{len(counter)} === company website added to mongo', 'green'))

                        item = get_from_mongo_url()

                        if item is None:
                            break
                        continue


                    google_url = f'https://www.google.com/search?q=site:{query_website} \"{cname.replace("&", " and ")}&hl=en&gl=united states&ie=UTF-8'

                    s.headers.update(header)
                    html_tor = s.get(google_url, timeout=10)
                    if html_tor.status_code == 200:
                        try:
                            url_ = sb_tor(html_tor.text, cname, social_network)

                            result = url_['url']

                            if (result != 'not exists'):
                                add_mongodb_social_network(cname, result, social_network)
                                print(colored('company_name : ' + cname + ' and ' + social_network + '_profile : ' + result + ' added to mongodb !', 'cyan'))

                            print(cname)
                            update_mongo_url(item['_id'], result)

                            counter.append('ok')
                            print(colored(f'{len(counter)} === company website added to mongo', 'green'))

                            item = get_from_mongo_url()

                            if item is None:
                                break
                            continue
                        except Exception as e:
                            print(e)
                    else:
                        print(colored(f'Process-{index}: {html_tor.status_code}', 'red'))
                        break
        except Exception as e:
            print(e)
            pass



def run_():
    pages = []
    number_processes = 30

    for i in range(1, number_processes + 1):
        pages.append(i)

    parts = chunkIt(pages, number_processes)

    processes = []

    for i in range(number_processes):
        # random_wait = random.random() * 3
        # time.sleep(random_wait)
        processes.append(multiprocessing.Process(target=find_sb, args=[parts[i], i]))

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

    print(false_count)
    print(process_count)


    if (false_count !=0 or process_count != 0):
        run_()
    print(colored('wait for ' + str(sleep_time) + ' seconds !!!', 'yellow'))

    time.sleep(sleep_time)


