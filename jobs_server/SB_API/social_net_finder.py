# new
import flask
import os.path

from lxml.html import clean
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
# import pythonwhois
import get_cert
import ssl
import urllib
from flask import Flask, session
from flask_session import Session
from urllib.parse import urljoin
import base64
import urllib

# no change_proxy

manager = multiprocessing.Manager()


country_list = ["Iran", "United Arab Emirates", "Argentina", "Austria", "Australia", "Belgium", "Brazil", "Canada", "Switzerland", "Chile", "China", "Columbia", "Czech Republic", "Germany", "Denmark", "Spain", "Finland", "France", "France, Metropolitan", "United Kingdom", "Greece", "Hong Kong", "Croatia", "Hungary", "Indonesia", "Ireland", "Israel", "India", "Iceland", "Italy", "Japan", "Lebanon", "Luxembourg", "Latvia", "Morocco", "Monaco", "Mexico", "Malaysia", "Netherlands", "Norway", "New Zealand", "Peru", "Philippines", "Pakistan", "Poland", "Puerto Rico", "Portugal", "Paraguay", "Qatar", "Romania", "Russian Federation", "Saudi Arabia", "Sweden", "Singapore", "Slovak Republic", "Thailand", "Turkey", "Taiwan", "Ukraine", "United States", "Uruguay", "Venezuela", "Vietnam", "Yugoslavia", "South Africa"]
country_code_list = ["ir", "ae", "ar", "at", "au", "be", "br", "ca", "ch", "cl", "cn", "co", "cz", "de", "dk", "es", "fi", "fr", "fx", "gb", "gr", "hk", "hr", "hu", "id", "ie", "il", "in", "is", "it", "jp", "lb", "lu", "lv", "ma", "mc", "mx", "my", "nl", "no", "nz", "pe", "ph", "pk", "pl", "pr", "pt", "py", "qa", "ro", "ru", "sa", "se", "sg", "sk", "th", "tr", "tw", "ua", "us", "uy", "ve", "vn", "yu", "za"]
language_2digits_list = ['aa', 'ab', 'ae', 'af', 'am', 'an', 'ar', 'as', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'ks', 'ku', 'kv', 'kw', 'ky', 'la', 'lb', 'li', 'ln', 'lo', 'lt', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']
language_3digits_list = ['aar', 'abk', 'ave', 'afr', 'amh', 'arg', 'ara', 'asm', 'aym', 'aze', 'bak', 'bel', 'bul', 'bih', 'bis', 'ben', 'tib', 'bre', 'bos', 'cat', 'che', 'cha', 'cos', 'cze', 'chu', 'chv', 'wel', 'dan', 'ger', 'div', 'dzo', 'gre', 'eng', 'epo', 'spa', 'est', 'baq', 'per', 'fin', 'fij', 'fao', 'fre', 'fry', 'gle', 'gla', 'glg', 'grn', 'guj', 'glv', 'hau', 'heb', 'hin', 'hmo', 'scr', 'hat', 'hun', 'arm', 'her', 'ina', 'ind', 'ile', 'iii', 'ipk', 'ido', 'ice', 'ita', 'iku', 'jpn', 'jav', 'geo', 'kik', 'kua', 'kaz', 'kal', 'khm', 'kan', 'kor', 'kas', 'kur', 'kom', 'cor', 'kir', 'lat', 'ltz', 'lim', 'lin', 'lao', 'lit', 'lav', 'mlg', 'mah', 'mao', 'mac', 'mal', 'mon', 'mol', 'mar', 'may', 'mlt', 'bur', 'nau', 'nob', 'nde', 'nep', 'ndo', 'dut', 'nno', 'nor', 'nbl', 'nav', 'nya', 'oci', 'orm', 'ori', 'oss', 'pan', 'pli', 'pol', 'pus', 'por', 'que', 'roh', 'run', 'rum', 'rus', 'kin', 'san', 'srd', 'snd', 'sme', 'sag', 'sin', 'slo', 'slv', 'smo', 'sna', 'som', 'alb', 'scc', 'ssw', 'sot', 'sun', 'swe', 'swa', 'tam', 'tel', 'tgk', 'tha', 'tir', 'tuk', 'tgl', 'tsn', 'ton', 'tur', 'tso', 'tat', 'twi', 'tah', 'uig', 'ukr', 'urd', 'uzb', 'vie', 'vol', 'wln', 'wol', 'xho', 'yid', 'yor', 'zha', 'chi', 'zul']


list_general_CUF = manager.list()
list_general_Linkedin = manager.list()


application = flask.Flask(__name__)

application.config["DEBUG"] = True


application.config.from_object(__name__)

#############################################################################################


################################## Search Engines ############################################

def google_search(companyName):
    if (companyName == None or companyName == ''):
        return [], []
    ####################################################
    print(colored('Send search request to google -> keyword : ' + companyName, 'green'))

    location = 'us'
    uule = 'United States'
    language = 'en'

    while True:

        url = "http://162.55.94.6:8897/all-serp-website?location=" + location + "&keyword=" + companyName +"&language=" + language + '&CUF_flag=Not Found'

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if (response.status_code == 200):
            if (response.json() == []):
                return [], []
            # return response.json()['organic_results']

            # return response.json()['organic_results'], response.json()['Knowledge_panel']
            try:
                return response.json()['organic_results'], response.json()['knowledge_panel']
            except Exception as e:
                print(e)
                return [], []
        else:
            continue

def google_search_socialnetwork(page_limit, companyName, location, language):

    if (companyName == None or companyName == ''):
        return []

    # query_website = 'wikipedia.org'
    # companyName = 'site:' + query_website + ' \"' + 'microsoft' + '\"'
    ####################################################

    while True:

        url = "http://162.55.94.6:8897/all-serp-website"

        querystring = {"language": "en", "location": "us", "search_engine": "google", "keyword": companyName, 'CUF_flag':'Not Found'}

        payload = ""
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if (response.status_code == 200):
            if (response.json() == []):
                return []
            return response.json()['organic_results']

##########################################################

def get_main_part_website(input_url):

    has_http = False
    has_https = False
    if ('http://' in input_url):
        has_http = True
        input_url = input_url.replace('http://', '')
    if ('https://' in input_url):
        has_https = True
        input_url = input_url.replace('https://', '')

    main_part_length = 1
    split_item = '/'
    split_list = str.split(input_url, split_item)

    out_string = ''
    for i in range(len(split_list)):
        out_string += split_list[i]
        if (i != len(split_list) - 1 and i < main_part_length - 1):
            out_string += split_item
        if (i == main_part_length - 1):
            break

    if (has_http):
        out_string = 'http://' + out_string
    if (has_https):
        out_string = 'https://' + out_string

    return out_string

    # if ((input_url.rsplit(yarl.URL(input_url).path_qs, 1)) != None and (input_url.rsplit(yarl.URL(input_url).path_qs, 1)) != ''):
    #     return ''.join(input_url.rsplit(yarl.URL(input_url).path_qs, 1))

def get_main_part_website_socialnetwork(input_url):
    has_http = False
    has_https = False
    if ('http://' in input_url):
        has_http = True
        input_url = input_url.replace('http://', '')
    if ('https://' in input_url):
        has_https = True
        input_url = input_url.replace('https://', '')

    main_part_length = 3
    split_item = '/'
    split_list = str.split(input_url, split_item)

    out_string = ''
    for i in range(len(split_list)):
        out_string += split_list[i]
        if (i != len(split_list) - 1 and i < main_part_length - 1):
            out_string += split_item
        if (i == main_part_length - 1):
            break

    if (has_http):
        out_string = 'http://' + out_string
    if (has_https):
        out_string = 'https://' + out_string

    # out_string = out_string.split('&')[0]
    return out_string

def notExistInBasicSites_db(site):


    try:
        client = MongoClient('localhost', 27017)
        db = client['basic_sites']
        collection = db['websites']

        for basic in collection.find():
            if basic['url'].strip() in site:
                return False
        return True


    except Exception as e:
        print(e)
        return False

def find_in_socialmedia(inputLink):

    if ('facebook.com' in inputLink):
        return True
    if ('instagram.com' in inputLink):
        return True
    if ('twitter.com' in inputLink):
        return True
    if ('linkedin.com' in inputLink):
        return True
    if ('pinterest.com' in inputLink):
        return True
    # if ('youtube.com' in inputLink):
    if ('youtube' in inputLink):
        return True
    if ('dnb.com/business-directory' in inputLink):
        return True
    if ('/company/' in inputLink or '/companies/' in inputLink or '/Company/' in inputLink or '/Companies/' in inputLink):
        return True
    if ('www.business-informations' in inputLink):
        return True
    if ('yelp.com' in inputLink):
        return True
    if ('map.search' in inputLink):
        return True
    if ('yellow.place' in inputLink or 'yellow.local' in inputLink or 'yellowpages' in inputLink):
        return True
    if ('.cylex' in inputLink):
        return True
    if ('winescholarguild.org' in inputLink):
        return True
    if ('winefunding.com' in inputLink):
        return True
    if ('wikiwand.com' in inputLink):
        return True
    if ('wikiart.org' in inputLink):
        return True
    if ('whoiskarendelacarriere.org' in inputLink):
        return True
    if ('https://www.walmart.com' in inputLink):
        return True
    if ('vivreenresidence.com' in inputLink):
        return True
    if ('vitisvintage.com' in inputLink):
        return True
    if ('vitisphere.com' in inputLink):
        return True
    if ('visit.alsace' in inputLink):
        return True
    if ('vignes.info' in inputLink):
        return True
    if ('unite22.com' in inputLink):
        return True
    if ('.uneautreloire.' in inputLink):
        return True
    if ('.twil.' in inputLink):
        return True
    if ('ter.sncf.com' in inputLink):
        return True
    if ('.spa-du-47.' in inputLink):
        return True
    if ('societe.com' in inputLink):
        return True
    if ('sirensiret.' in inputLink):
        return True
    if ('saq.com' in inputLink):
        return True
    if ('residencescogir.com.' in inputLink):
        return True
    if ('plaimont.com.' in inputLink):
        return True
    if ('napaautopro.com' in inputLink):
        return True
    if ('metro.ca' in inputLink):
        return True
    if ('le-saint-remy.' in inputLink):
        return True
    if ('frankfurt-trophy.com' in inputLink):
        return True
    if ('infogreffe.fr' in inputLink):
        return True
    if ('gardencommunitiesca.com' in inputLink):
        return True
    if ('infogreffe.' in inputLink):
        return True
    if ('gites-de-france.com.' in inputLink):
        return True
    if ('hdmedia.' in inputLink):
        return True
    if ('concoursgamay.com' in inputLink):
        return True
    if ('concourscabernets.com' in inputLink):
        return True
    if ('avenuedesvins.' in inputLink):
        return True
    if ('agriculture.' in inputLink):
        return True
    if ('francetourismes.wordpress.com' in inputLink):
        return True
    if ('verifsociete.' in inputLink):
        return True
    if ('1001degustations.' in inputLink):
        return True
    if ('france-enterprise.' in inputLink):
        return True
    if ('chablis.' in inputLink):
        return True
    if ('france-amerique.' in inputLink):
        return True
    if ('assemblee-nationale.' in inputLink):
        return True
    if ('entreprises.lefigaro' in inputLink):
        return True
    if ('champagne-destination-damien-buffet.' in inputLink):
        return True
    if ('france-amerique.' in inputLink):
        return True
    if ('gite-de-la-porte-du-parc-holiday-home.allbrittanyhotels.' in inputLink):
        return True

    return False

def get_valid_top_list(input_list):

    out_set = []

    if (len(input_list) ==0):
        return out_set

    for i in range(len(input_list)):
        if (len(out_set) >= 4):
            return out_set

        set_json = {}
        set_json['input_url'] = input_list[i]['url']
        set_json['main_url'] = get_main_part_website(input_list[i]['url'])
        set_json['title'] = input_list[i]['title']
        out_set.append(set_json)


    return out_set

def get_set_list_social_network(input_list, companyName, social_network):

    out_set = []

    if (input_list == None or len(input_list) == 0 ):
        return out_set

    item = input_list[0]

    if (social_network == 'Twitter' and 'twitter.com/' not in item['url']):
        return out_set
    elif (social_network == 'Facebook' and 'facebook.com/' not in item['url']):
        return out_set
    elif (social_network == 'Instagram' and 'instagram.com/' not in item['url']):
        return out_set
    elif (social_network == 'Linkedin' and 'linkedin.com/' not in item['url']):
        return out_set
    elif (social_network == 'Myspace' and 'myspace.com/' not in item['url']):
        return out_set
    elif (social_network == 'Plaxo' and 'plaxo.com/' not in item['url']):
        return out_set
    elif (social_network == 'Tumblr' and 'tumblr.com/' not in item['url']):
        return out_set
    elif (social_network == 'Livejournal' and 'livejournal.com/' not in item['url']):
        return out_set
    elif (social_network == 'Flickr' and 'flickr.com/' not in item['url']):
        return out_set
    elif (social_network == 'Youtube' and 'youtube.com/' not in item['url']):
        return out_set
    elif (social_network == 'Pinterest' and 'pinterest.com/' not in item['url']):
        return out_set
    elif (social_network == 'Vimeo' and 'vimeo.com/' not in item['url']):
        return out_set
    elif (social_network == 'Spotify' and 'spotify.com/' not in item['url']):
        return out_set
    elif (social_network == 'Twitch' and 'twitch.tv/' not in item['url']):
        return out_set
    elif (social_network == 'Telegram' and 't.me/' not in item['url']):
        return out_set
    elif (social_network == 'WhatsApp' and 'whatsapp.com/' not in item['url']):
        return out_set
    elif (social_network == 'WeChat' and 'wechat.com/' not in item['url']):
        return out_set
    elif (social_network == 'TikTok' and 'tiktok.com/' not in item['url']):
        return out_set
    elif (social_network == 'Snapchat' and 'snapchat.com/' not in item['url']):
        return out_set
    elif (social_network == 'Reddit' and 'reddit.com/' not in item['url']):
        return out_set
    elif (social_network == 'Wikipedia' and 'wikipedia.org/' not in item['url']):
        return out_set
    elif (social_network == 'IMDb' and 'imdb.com/' not in item['url']):
        return out_set
    elif (social_network == 'Github' and 'github.com/' not in item['url']):
        return out_set
    elif (social_network == 'Booking' and 'booking.com/' not in item['url']):
        return out_set
    elif (social_network == 'GoogleScholar' and 'scholar.google.com/' not in item['url']):
        return out_set
    elif (social_network == 'Crunchbase' and 'crunchbase.com/organization/' not in item['url']):
        return out_set
    elif (social_network == 'Zoominfo' and 'zoominfo.com/c/' not in item['url']):
        return out_set
    elif (social_network == 'StackOverflow' and 'stackoverflow.com/users/' not in item['url']):
        return out_set
    elif (social_network == 'Amazon' and 'amazon.com/stores/' not in item['url']):
        return out_set

    companyName_tokens = companyName.split(' ')
    len_total = len(companyName_tokens)
    token_passed = 0

    for token in companyName_tokens:
        if token.strip().lower() in item['title'].replace(' ','').lower():
            token_passed += 1
    if (token_passed >= 2 or token_passed/len_total > 0.5):

        out_set.append(item['url'].split('&')[0])

    return out_set

def weight_search_engine_output_social_network(out_result, companyName, social_network):

    set_company = get_set_list_social_network(out_result, companyName, social_network)
    return set_company

def insert_requests_db(input_json):
    try:
        pass


    except Exception as e:
        print(e)

def add_mongodb(selected_website):

    try:
        client_company_web = MongoClient('localhost', 27017)
        db_company_web = client_company_web['company_web_collection']
        collection_company_web = db_company_web['websites']
        updateJson ={'company_name': selected_website['query'].lower(), 'url': selected_website['url']}

        find_record = collection_company_web.find_one({'company_name': selected_website['query'].lower()})
        if (find_record == None):
            collection_company_web.insert_one(updateJson)
        client_company_web.close()

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

def check_mongodb_exist(companyName):

    companyName = companyName.lower()
    client_company_web = MongoClient('mongodb://localhost:27017')

    try:
        db_company_web = client_company_web['company_web_collection']
        collection_company_web = db_company_web['websites']

        find_in_db_lower = collection_company_web.find_one({'company_name': companyName})
        client_company_web.close()

        if (find_in_db_lower == None):
            return None
        elif find_in_db_lower != None:

            return find_in_db_lower


    except Exception as e:
        print (colored(e,'red'))
        client_company_web.close()
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

def select_valid_slash_based(input_url, search_list, companyName, index):

    # replace end'/', www., http:// and https://
    if (input_url[-1] == '/'):
        input_url = input_url[0:-1]
    input_url = input_url.replace('www.','').replace('http://','').replace('https://','')

    # split with /
    item_list = input_url.split('/')

    # with one /
    if (len(item_list) == 1):
        return search_list[index]['input_url']

    # with two /
    if (len(item_list) == 2):
        second_item = item_list[1].strip().lower()

        if ('/default' in input_url or '/en/' in input_url or 'en-' in input_url or '_en' in input_url or second_item.startswith('#') or 'home' in second_item or 'index' in second_item or'contact' in second_item or 'about' in second_item or second_item in country_list or second_item in country_code_list or second_item in language_2digits_list or second_item in language_3digits_list):
            return search_list[index]['input_url']

    # with more two /
    elif (len(item_list) > 2):
        domain_split_list = item_list[0].split('.')
        domain = ''
        for i in range(len(domain_split_list)-1):
            if (i==len(domain_split_list)-2):
                domain += domain_split_list[i]
            else:
                domain += domain_split_list[i] + '.'
        domain = domain.strip().replace('-', '')

        # check domain in companyname for more two /
        if ((('/default' in input_url or '/en/' in input_url or 'en-' in input_url or '_en' in input_url) and len(item_list) == 3 ) or (domain.lower() in companyName.replace(' ','').replace('-', '').lower())):
            return search_list[index]['input_url']

    return None

def select_module_slash_social(search_list, companyName):

    out_list = []

    if (search_list ==[]):
        return out_list


    for index, item in enumerate(search_list):
        selected_website = item['input_url']

        if (find_in_socialmedia(selected_website) or not notExistInBasicSites_db(selected_website)): # ignore social network urls
            continue
        else:
            selected_url= select_valid_slash_based(selected_website, search_list, companyName, index)
            if (selected_url != None):
                out_list.append(selected_url)


    return out_list

def check_knowledge_panel_website (knowledge_panel_list):

    knowledge_panel_info_json={}
    Website = None
    Address = None
    social_network = None

    for kp in knowledge_panel_list:
        for item in kp:
            item_clear = item.replace(':', '').strip()
            if (item_clear in knowledge_panel_info_json):
                continue

            if item_clear == 'Address':
                Address = kp[item]
            elif item_clear == 'Website':
                Website = kp[item]
            elif item_clear == 'social_network':
                social_network = kp[item]

            knowledge_panel_info_json[item_clear] = kp[item]

    return Website

def company_website_finder (companyName, ip_add_remote, DB_flag, multi_process_flag):

    if (str(DB_flag) == 'True' or str(DB_flag) == 'true' or str(DB_flag) == 'TRUE'):
        find_in_db = check_mongodb_exist(companyName)
    else:
        find_in_db = False

    if (find_in_db and ('url' in find_in_db)):
        print(colored('company_name : ' + companyName + ' already exists in mongodb !', 'green'))
        out_json = {'query' : companyName, 'url' : find_in_db['url']}

        if (multi_process_flag):
            list_general_CUF.append(out_json['url'])

        return out_json

    ###########################################################################################################


    google_organic_results, KPs = google_search(companyName)


    print (colored('==================================== Weighting ==========================================','magenta'))

    # check website existed in the knowledge panel of google search
    kp_website_find = check_knowledge_panel_website(KPs)

    if (kp_website_find):
        json_out = {}
        json_out['query'] = companyName
        json_out['url'] = kp_website_find

        if (multi_process_flag):
            list_general_CUF.append(json_out['url'])

        if (json_out['url'] != None and json_out['url'] != 'Not Found'):
            add_mongodb(json_out)
            print(colored('company_name : ' + companyName + ' and company_website : ' + str(json_out['url']) + ' added to mongodb !', 'green'))

        return json_out

    else:
        selected_website_google_list = get_valid_top_list(google_organic_results) # return top 4 organic urls
        selected_website_list = select_module_slash_social(selected_website_google_list, companyName)

    ####

    json_out = {}
    json_out['query'] = companyName
    json_out['url'] = 'Not Found'


    for item in selected_website_list:
        json_out['url'] = get_main_part_website(item)
        break # only return one value

    if (json_out['url'] != None and json_out['url'] != 'Not Found'):
        add_mongodb(json_out)
        print(colored('company_name : ' + companyName + ' and company_website : ' + str(json_out['url']) + ' added to mongodb !', 'green'))

    if (multi_process_flag):
        list_general_CUF.append(json_out['url'])

    return (json_out)

def company_social_network_finder (companyName, social_network):

    init_time = datetime.datetime.now()

    client = MongoClient('localhost', 27017)

    find_in_db = check_mongodb_exist_social_network(companyName, social_network)
    # find_in_db = False

    if (len(companyName) <= 2):
        json_out = {'query': companyName, 'url': 'not exists'}
        return json_out

    if (find_in_db and ('company_website' in find_in_db)):
        print(colored('company_name : ' + companyName + ' already exists in mongodb !', 'green'))
        website_db = find_in_db['company_website']
        json_out = {'query' : companyName, 'url': website_db}
        return json_out


    location = 'us'
    language = 'en'

    try_limit = 1
    try_count =0

    while try_count < try_limit:

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
            json_out = {}
            json_out['query'] = companyName
            json_out['url'] = 'not exists'
            return json_out


        print (colored('Send search request to google -> keyword : site:' + query_website + ' \"' + companyName + '\" try: ' + str(try_count),'green'))
        # GOOGLE
        try:
            out_result_google_company = google_search_socialnetwork(page_limit, 'site:' + query_website + ' \"' + companyName + '\"', location, language)
        except Exception as e:
            print(e)
            out_result_google_company = []

        if (len(out_result_google_company) ==0):
            try_count += 1
            continue
        else:
            break

    ###########################################################################################################
    print (colored('==================================== ' + social_network +' Weighting ==========================================','magenta'))

    weighted_list = weight_search_engine_output_social_network(out_result_google_company, companyName, social_network)
    selected_website = weighted_list



    ############################################################################################################
    json_out = {}

    if (selected_website == 'Search list is empty !!!' or len(selected_website) == 0):

        json_out['query'] = companyName
        json_out['url'] = 'not exists'

        return (json_out)

    for item in selected_website:
        json_out['query'] = companyName
        json_out['url'] = item
        break # only return one value

    if ('url' in json_out and json_out['url'] != 'not exists'):
        add_mongodb_social_network(companyName, json_out['url'], social_network)
        print(colored('company_name : ' + companyName + ' and ' + social_network + '_profile : ' + str(selected_website[0]) + ' added to mongodb !', 'cyan'))

    return (json_out)

############################### Global Variables #######################################################

process_num = 1
time_out = 10
page_limit = 1



@application.route('/company_url_finder',methods=['GET','POST'])
def start():

    companyName = flask.request.args.get('companyName', default='', type=str)
    DB_flag = flask.request.args.get('DB_flag', default='True', type=str)

    ip_add_remote = flask.request.remote_addr

    if (companyName =='' or companyName == None):
        print('Invalid companyName !!!')
        json_out = {}
        json_out['query'] = companyName
        json_out['url'] = 'Not Found'
        return json_out


    multi_process_flag = False

    return flask.jsonify(company_website_finder(companyName, ip_add_remote, DB_flag, multi_process_flag))








@application.route('/company_social_network_finder',methods=['GET','POST'])
def start_social_network():

    companyName = flask.request.args.get('companyName', default='', type=str)
    social_network = flask.request.args.get('social_network', default='', type=str)

    ip_add_remote = flask.request.remote_addr

    if (companyName =='' or companyName == None):
        print('Invalid companyName !!!')
        json_out = {}
        json_out['query'] = companyName
        json_out['url'] = 'not exists'
        return json_out

    if (social_network =='' or social_network == None):
        print('Invalid social_network !!!')
        json_out = {}
        json_out['query'] = companyName
        json_out['url'] = 'not exists'
        return json_out

    return company_social_network_finder(companyName, social_network)

if __name__ == "__main__":
    application.run(host='0.0.0.0', threaded = True)
    # modify_CUF_db()


