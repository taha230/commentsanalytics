# v.1
from termcolor import colored
import validators
import requests
from bs4 import BeautifulSoup
import re
from itertools import groupby
import yarl
from urllib.parse import urljoin
from torpy.http.requests import tor_requests_session
import commonregex
import phonenumbers
import pycountry
from phone_iso3166.country import phone_country
from pymongo import MongoClient
import tldextract
import random
import os



CHAR_HTML_LIMIT = 500000

country_list = ["Iran", "United Arab Emirates", "Argentina", "Austria", "Australia", "Belgium", "Brazil", "Canada", "Switzerland", "Chile", "China", "Columbia", "Czech Republic", "Germany", "Denmark", "Spain", "Finland", "France", "France, Metropolitan", "United Kingdom", "Greece", "Hong Kong", "Croatia", "Hungary", "Indonesia", "Ireland", "Israel", "India", "Iceland", "Italy", "Japan", "Lebanon", "Luxembourg", "Latvia", "Morocco", "Monaco", "Mexico", "Malaysia", "Netherlands", "Norway", "New Zealand", "Peru", "Philippines", "Pakistan", "Poland", "Puerto Rico", "Portugal", "Paraguay", "Qatar", "Romania", "Russian Federation", "Saudi Arabia", "Sweden", "Singapore", "Slovak Republic", "Thailand", "Turkey", "Taiwan", "Ukraine", "United States", "Uruguay", "Venezuela", "Vietnam", "Yugoslavia", "South Africa"]
country_code_list = ["ir", "ae", "ar", "at", "au", "be", "br", "ca", "ch", "cl", "cn", "co", "cz", "de", "dk", "es", "fi", "fr", "fx", "gb", "gr", "hk", "hr", "hu", "id", "ie", "il", "in", "is", "it", "jp", "lb", "lu", "lv", "ma", "mc", "mx", "my", "nl", "no", "nz", "pe", "ph", "pk", "pl", "pr", "pt", "py", "qa", "ro", "ru", "sa", "se", "sg", "sk", "th", "tr", "tw", "ua", "us", "uy", "ve", "vn", "yu", "za"]
language_2digits_list = ['aa', 'ab', 'ae', 'af', 'am', 'an', 'ar', 'as', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'ks', 'ku', 'kv', 'kw', 'ky', 'la', 'lb', 'li', 'ln', 'lo', 'lt', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz',
                         'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']
language_3digits_list = ['aar', 'abk', 'ave', 'afr', 'amh', 'arg', 'ara', 'asm', 'aym', 'aze', 'bak', 'bel', 'bul', 'bih', 'bis', 'ben', 'tib', 'bre', 'bos', 'cat', 'che', 'cha', 'cos', 'cze', 'chu', 'chv', 'wel', 'dan', 'ger', 'div', 'dzo', 'gre', 'eng', 'epo', 'spa', 'est', 'baq', 'per', 'fin', 'fij', 'fao', 'fre', 'fry', 'gle', 'gla', 'glg', 'grn', 'guj', 'glv', 'hau', 'heb', 'hin', 'hmo', 'scr', 'hat', 'hun', 'arm', 'her', 'ina', 'ind', 'ile', 'iii', 'ipk', 'ido', 'ice', 'ita', 'iku', 'jpn', 'jav', 'geo', 'kik', 'kua', 'kaz', 'kal', 'khm', 'kan', 'kor', 'kas', 'kur', 'kom', 'cor', 'kir', 'lat', 'ltz', 'lim', 'lin', 'lao', 'lit', 'lav', 'mlg', 'mah', 'mao', 'mac', 'mal', 'mon', 'mol', 'mar', 'may', 'mlt', 'bur', 'nau', 'nob', 'nde', 'nep', 'ndo', 'dut', 'nno', 'nor', 'nbl', 'nav', 'nya', 'oci', 'orm', 'ori', 'oss', 'pan', 'pli', 'pol', 'pus', 'por', 'que', 'roh', 'run', 'rum', 'rus', 'kin', 'san', 'srd', 'snd', 'sme', 'sag', 'sin', 'slo', 'slv', 'smo', 'sna', 'som', 'alb',
                         'scc', 'ssw', 'sot', 'sun', 'swe', 'swa', 'tam', 'tel', 'tgk', 'tha', 'tir', 'tuk', 'tgl', 'tsn', 'ton', 'tur', 'tso', 'tat', 'twi', 'tah', 'uig', 'ukr', 'urd', 'uzb', 'vie', 'vol', 'wln', 'wol', 'xho', 'yid', 'yor', 'zha', 'chi', 'zul']


# no change_proxy



def change_proxy_bank():

    while True:
        try:
            client = MongoClient('localhost', 27017)
            db = client['proxy_bank_collection']
            collection = db['bank']

            current_count = collection.count()
            if (current_count > 0):
                shuffle_index =  int(random.random() * (current_count-1))
                # most_new_row = collection.find().sort([("time_slot", -1)])[shuffle_index] # get proxy shuffle
                most_new_row = collection.find().sort([("time_slot", -1)])[0] # get proxy shuffle
                # collection.delete_one(most_new_row)
                client.close()
                print(colored('get proxy from Proxy Bank !!! (count : '+ str(current_count)+ ')'))
                return most_new_row['proxy'], most_new_row['useragent']

            else:
                print(colored('Waiting for filling Proxy Bank','magenta'))
                continue



        except Exception as e:
            print(e)

def projection_class (val):
    return val.attrs['class']

def projection_len (val):
    return len(val)

def google_extract_info(html, keyword, language, location, number, page_limit, api_key, near):
    # out_json ={}
    # out_json['organic_results'] = ['a']
    # out_json['ad_results'] = []
    # out_json['video_results'] = []
    # out_json['related_question_results'] = []
    #
    # return out_json

    out_json = {}
    url_results = []
    url_results_adv = []
    url_results_video = []
    question_list = []
    result_per_page = number

    url_results_page = []
    url_results_adv_page = []
    url_results_video_page = []
    question_list_page = []
    related_search_list_page = []
    knowledge_panel_page = {}
    related_search_list = []
    knowledge_panel_list = []
    local_results = []

    out_json['pagination'] = {'current': page_limit, 'next': '', 'other_pages': []}

    try:

        content = html
        # content = (open("deeplite.txt", "r").read()).encode('utf_8')
        soup = BeautifulSoup(content, 'html.parser')

        ##### break condition
        if ('did not match any documents' in str(content)):
            # print(colored('did not match any documents', 'red'))

            out_json['organic_results'] = url_results
            out_json['ad_results'] = url_results_adv
            out_json['video_results'] = url_results_video
            out_json['related_search'] = related_search_list
            out_json['people_also_asked'] = question_list
            out_json['Knowledge_panel'] = knowledge_panel_list
            out_json['local_results'] = local_results

            return out_json

        h3List_has_span = []
        for h3 in soup.find_all('h3', attrs={'class': True, 'roll': False}):

            if (not h3.find('a')):
                h3List_has_span.append(h3)

        if (len(h3List_has_span) > 0):

            result_title = sorted([list(it) for k, it in groupby(sorted(h3List_has_span, key=projection_class), projection_class)], key=projection_len)[-1]

            result_num = 1
            for item in result_title:
                result_json = {}
                if (len(url_results_page) == result_per_page):
                    break
                if (item.parent and ('href=' in str(item.parent))):

                    if (item.parent.parent and item.parent.parent.parent):

                        parent_parent_text = item.parent.parent.text
                        total_text = item.parent.parent.parent.text
                        url = ''
                        url = item.parent['href'].replace('/url?q=', '').split('&sa=U')[0].split('%')[0].split('%')[0]

                        # if ('href=' in str(item.parent)):
                        # if('href=' in str(item.parent.parent)):
                        #     url = item.parent.parent['href'].replace('/url?q=', '').split('&sa=U')[0].split('%')[0].split('%')[0]

                        if ('.google.' not in url and '.googleusercontent.' not in url):
                            result_json['keyword'] = keyword
                            result_json['language'] = language
                            result_json['location'] = location
                            result_json['url'] = url.strip()
                            result_json['page_query'] = page_limit
                            result_json['number_query'] = number
                            result_json['position'] = result_num
                            result_json['title'] = item.text.strip()
                            result_json['body'] = total_text.replace(parent_parent_text, '').strip()

                            url_results_page.append(result_json)
                            result_num += 1


        else:  # h3 list is empty

            # mode 2 organic search

            # print (colored(str(html_content) , 'cyan'))

            div_main = soup.find('div', id='main')
            if (div_main):
                result_num = 1

                a_list = div_main.find_all('a', href=True)
                for a_tag in a_list:

                    result_json = {}
                    if (len(url_results_page) == result_per_page):
                        break

                    div_list = a_tag.find_all('div', href=True)
                    if (len(div_list) == 2):
                        url = a_tag['href'].replace('/url?q=', '')
                        if ('.google.' not in url and '.googleusercontent.' not in url):
                            result_json['keyword'] = keyword
                            result_json['language'] = language
                            result_json['location'] = location
                            result_json['url'] = url.replace('/url?q=', '').split('&sa=U')[0].split('%')[0].strip()
                            result_json['page_query'] = page_limit
                            result_json['number_query'] = number
                            result_json['position'] = result_num
                            result_json['title'] = div_list[0].text.strip()
                            result_json['body'] = ''
                            url_results_page.append(result_json)
                            result_num += 1

        if (len(url_results_page) == 0):
            print(colored('process: >>>> google result is empty !', 'red'))

            out_json['organic_results'] = url_results
            out_json['ad_results'] = url_results_adv
            out_json['video_results'] = url_results_video
            out_json['related_search'] = related_search_list
            out_json['people_also_asked'] = question_list
            out_json['Knowledge_panel'] = knowledge_panel_list
            out_json['local_results'] = local_results

            return out_json

        # Advertisement
        advList = soup.find_all('li', class_='ads-ad')
        adv_position = 1
        for adv in advList:
            aList = adv.find_all('a', href=True)
            for a in aList:
                if (a.find('h3')):
                    adv_json = {}

                    adv_json['url'] = a['href'].replace('/url?q=', '').split('&sa=U')[0].split('%')[0]
                    adv_json['title'] = a.find('h3').text.strip()
                    adv_json['position'] = adv_position
                    adv_json['page_query'] = page_limit
                    adv_json['number_query'] = number
                    url_results_adv_page.append(adv_json)

                    adv_position += 1

        # adv mode 2
        if (len(advList) == 0):
            for ad in soup.find_all('span', text='Ad'):
                if (ad.parent.parent):
                    adv_json = {}

                    # if ('href' in str(ad.parent.parent)):
                    #     adv_json['url'] = ad.parent.parent['href']
                    adv_json['url'] = ''
                    for span in ad.parent.find_all('span'):
                        if (span.text.strip() != 'Ad'):
                            adv_json['url'] = span.text.replace('/url?q=', '').split('&sa=U')[0].split('%')[0].strip()
                            break

                    if (ad.parent.parent.find('div', role='heading')):
                        adv_json['title'] = ad.parent.parent.find('div', role='heading').text.strip()

                    adv_json['position'] = adv_position
                    result_json['page_query'] = page_limit
                    result_json['number_query'] = number
                    url_results_adv_page.append(adv_json)

                    adv_position += 1

        # adv mode 3
        if (len(advList) == 0):
            for adv in soup.findAll('div', attrs={"data-text-ad": '1'}):
                if (adv.parent.parent):
                    adv_json = {}

                    if (adv.find('a', href=True)):
                        adv_json['url'] = adv.find('a', href=True)['href']

                    if (adv.find('div', role='heading')):
                        adv_json['title'] = adv.find('div', role='heading').text.strip()

                    adv_json['position'] = adv_position
                    result_json['page_query'] = page_limit
                    result_json['number_query'] = number
                    url_results_adv_page.append(adv_json)

                    adv_position += 1

        # videos
        videoList = soup.find_all('div', class_='V1Ddwd')
        video_position = 1
        for video in videoList:
            if (video.parent and video.parent.parent and video.parent.parent.parent and video.parent.parent.parent.parent and 'href=' in str(video.parent.parent.parent.parent) and video.parent.parent.parent.parent.find('div', role='heading')):
                video_url = video.parent.parent.parent.parent['href']
                video_title = video.parent.parent.parent.parent.find('div', role='heading').text.strip()

                video_json = {}
                video_json['video_url'] = video_url
                video_json['video_title'] = video_title
                video_json['position'] = video_position
                video_json['page_query'] = page_limit
                video_json['number_query'] = number

                video_position += 1
                url_results_video_page.append(video_json)

        # video mode 2
        if (len(url_results_video_page) == 0):
            for video in soup.findAll('div', role='heading', href=False):
                if (video.parent and video.parent.parent and video.parent.parent.parent and video.parent.parent.parent.parent and video.findChild() == None and video.text.strip() == video.parent.text.strip()):

                    if (video.parent.parent.parent.parent.get('href') == None):
                        continue
                    video_url = video.parent.parent.parent.parent['href']
                    video_title = video.parent.parent.parent.parent.find('div', role='heading').text.strip()

                    video_json = {}
                    video_json['video_url'] = video_url
                    video_json['video_title'] = video_title
                    video_json['position'] = video_position
                    video_json['page_query'] = page_limit
                    video_json['number_query'] = number
                    url_results_video_page.append(video_json)
                    video_position += 1

        relatedQuestionsList = soup.find_all('div', class_='related-question-pair')

        # mode 2 People also ask
        if (len(relatedQuestionsList) == 0):

            h2_people_also_ask = soup.find('h2', text='People also ask')
            if (h2_people_also_ask):
                for div in h2_people_also_ask.parent.find_all('div', text=True):
                    relatedQuestionsList.append(div)

        question_position = 1
        # if (len(relatedQuestionsList) == 0):
        # print (colored(str(html_content) , 'cyan'))

        for question in relatedQuestionsList:
            question_json = {}
            question_json['question_text'] = question.text.strip()
            if (question_json['question_text'] == 'People also ask'):
                continue
            question_json['position'] = question_position
            question_json['page_query'] = page_limit
            question_json['number_query'] = number

            question_position += 1
            question_list_page.append(question_json)

        # mode 1 related search
        relatedSearchsList = []
        for a in soup.find_all('a', href=re.compile(r'/search?sxsrf.*')):
            if a.find('b'):
                relatedSearchsList.append(a)

        # mode 2 related search
        if (len(relatedSearchsList) == 0):
            div_related_search = soup.find('div', text='Related searches')
            if (div_related_search):
                if (div_related_search.parent.parent.parent.parent):
                    for div in div_related_search.parent.parent.parent.parent.find_all('div', text=True):

                        if div.find('span', text=True):
                            if (div.find_all('div')):
                                if len(div.find_all('div')) == 1:
                                    relatedSearchsList.append(div)
        # mode 3 related search
        if (len(relatedSearchsList) == 0):
            div_related_search = soup.find('div', class_='card-section')
            if (div_related_search):
                for p in div_related_search.find_all('p'):

                    if p.find('a', href=True) and p.find('a', href=True).text.strip() == p.text.strip():
                        relatedSearchsList.append(p)

        search_position = 1
        for search in relatedSearchsList:
            search_json = {}
            search_json['related_search_text'] = search.text.strip()
            search_json['position'] = search_position
            search_json['page_query'] = page_limit
            search_json['number_query'] = number

            search_position += 1
            related_search_list_page.append(search_json)

        ###################################################################
        # Knowledge panel

        kp_header_div = soup.find('div', class_="kp-header")
        if kp_header_div == None:
            kp_header_div = soup.find('div', class_='kp-wholepage')

        if (kp_header_div and kp_header_div.parent):
            for a in kp_header_div.parent.find_all('a'):
                if a.parent and ':' in a.parent.text:
                    if (a.parent.parent):
                        key = a.text.strip()
                        value = a.parent.parent.text.replace(key + ' :', '').replace(key + ':', '').strip()
                        if ('Phone' in key):
                            if ('+' not in value):
                                value = '+1 ' + value
                        if (key == 'Hours'):
                            value = value.replace('Suggest an editUnable to add this file.', '') \
                                .replace('Please check that it is a valid photo.', '') \
                                .replace('Closes soon ⋅', '') \
                                .replace('PM', ' PM ').replace('AM', ' AM ').strip() \
                                .replace('Saturday', ', Saturday ') \
                                .replace('Sunday', ', Sunday ') \
                                .replace('Monday', ', Monday ') \
                                .replace('Tuesday', ', Tuesday ') \
                                .replace('Wednesday', ', Wednesday ') \
                                .replace('Thursday', ', Thursday ') \
                                .replace('Friday', ', Friday ')
                        if ('Missing:' != key and '$' not in value and '$' not in key and '\\' not in key and ('\\' not in kp_header_div.text or 'function()' in kp_header_div.text) and value != '' and key != '' and '.' not in key and value != '.' and key.replace(':', '').strip() not in knowledge_panel_page):
                            knowledge_panel_page[key] = value
                else:
                    continue

        # Description
        if (kp_header_div and kp_header_div.parent):
            h_desscription = kp_header_div.parent.find('h2', text='Description')
            if (h_desscription and h_desscription.parent):
                description_text = h_desscription.parent.text.replace('Description', '').split('. Wikipedia')[0].strip()
                if (description_text != '' and ':' not in description_text ):
                    knowledge_panel_page['Description'] = description_text

        # Website
        website_a = soup.find('a', attrs={"data-attrid": "visit_official_site"}, href=True)

        if (website_a):
            knowledge_panel_page['Website'] = website_a.get('href').split('?')[0]
        else:
            website_div = soup.find('a', text='Website', href=True)
            if (website_div and website_div.get('href')):
                knowledge_panel_page['Website'] = website_div.get('href').split('?')[0]

            else:
                website_div = soup.find('div', text='Website')
                if (website_div and website_div.parent and website_div.parent.parent):
                    a_parent_website = website_div.parent.parent
                    if (a_parent_website):
                        if (a_parent_website.get('href')):
                            knowledge_panel_page['Website'] = a_parent_website.get('href').split('?')[0]

        # Social Network Profiles
        if (kp_header_div and kp_header_div.parent):
            profiles_div = kp_header_div.parent.find('div', text='Profiles')
            if (profiles_div and profiles_div.parent):
                social_network_json = {}
                for a in profiles_div.parent.find_all('a', href=True):
                    if ('youtube.com' in a.get('href')):
                        social_network_json['youtube_profile'] = a.get('href')
                    elif ('linkedin.com/company/' in a.get('href')):
                        social_network_json['linkedin_profile'] = a.get('href')
                    elif ('twitter.com' in a.get('href')):
                        social_network_json['twitter_profile'] = a.get('href')
                    elif ('facebook.com' in a.get('href')):
                        social_network_json['facebook_profile'] = a.get('href')
                    elif ('instagram.com' in a.get('href')):
                        social_network_json['instagram_profile'] = a.get('href')

                knowledge_panel_page['social_network'] = social_network_json

        ###################################################################
        # Knowledge panel mode 2 - website
        kp_div = None

        if ('Website' not in knowledge_panel_page):
            if (soup.find('div', text='Website') and soup.find('div', text='Website').parent.parent.parent.parent.parent):
                kp_div = soup.find('div', text='Website').parent.parent.parent.parent.parent
                if ('href' in str(kp_div.find('div', text='Website').parent)):
                    knowledge_panel_page['Website'] = kp_div.find('div', text='Website').parent['href'].split('&')[0].replace('/url?q=', '').split('&sa=U')[0].split('%')[0].strip()
            elif soup.find_all('h3'):
                for h3 in soup.find_all('h3'):
                    if (h3.find('div') and h3.text == h3.find('div').text and h3.parent.parent and h3.parent.parent.find('a') and 'href' in h3.parent.parent.find('a')):
                        knowledge_panel_page['Website'] = h3.parent.parent.find('a')['href'].split('&')[0].replace('/url?q=', '').split('&sa=U')[0].split('%')[0].strip()
                        break

            # Knowledge panel mode 2 - description
            if ('Description' not in knowledge_panel_page):
                if (soup.find('span', text='Wikipedia') and soup.find('span', text='Wikipedia').parent.parent.parent):
                    knowledge_panel_page['Description'] = soup.find('span', text='Wikipedia').parent.parent.parent.text.replace('. Wikipedia', '.').strip()

            # if (soup.find('div', text = 'Website').parent.parent.parent.parent.parent or soup.find('div', text = 'Directions').parent.parent.parent.parent.parent )
            #     if (soup.find('div', text='Website').parent.parent.parent.parent.parent):
            #         kp_div = soup.find('div', text = 'Website').parent.parent.parent.parent.parent
            #     elif (soup.find('div', text='Directions').parent.parent.parent.parent.parent):
            #         kp_div = soup.find('div', text = 'Directions').parent.parent.parent.parent.parent

            for div in soup.find_all('div'):
                if (div.find('div') or ':' not in div.text):
                    continue

                span_list_total = div.find_all('span')

                span_list = []
                for span in span_list_total:
                    if (span.find('span')):
                        continue
                    span_list.append(span)

                if len(span_list) >= 2:

                    key = span_list[0].text.strip()

                    value_total = ''
                    for i in range(1, len(span_list)):
                        value = span_list[i].text.strip()

                        if ('Phone' in key):
                            if ('+' not in value):
                                value = '+1 ' + value
                        if (key == 'Hours'):
                            value = value.replace('Suggest an editUnable to add this file.', '') \
                                .replace('Please check that it is a valid photo.', '') \
                                .replace('Closes soon ⋅', '') \
                                .replace('PM', ' PM ').replace('AM', ' AM ').strip() \
                                .replace('Saturday', ', Saturday ') \
                                .replace('Sunday', ', Sunday ') \
                                .replace('Monday', ', Monday ') \
                                .replace('Tuesday', ', Tuesday ') \
                                .replace('Wednesday', ', Wednesday ') \
                                .replace('Thursday', ', Thursday ') \
                                .replace('Friday', ', Friday ')
                        if (value_total != ''):
                            value_total += ','
                        value_total += value

                    if ('Missing:' != key and '$' not in value and '$' not in key and '\\' not in key  and '\\' not in value and value != '' and key != '' and '.' not in key and value != '.' and key.replace(':', '').strip() not in knowledge_panel_page):
                        knowledge_panel_page[key] = value_total

        # ignore inline key and value that has : inside the value (Ex . ADDDF in Stock price: ADDDF (OTCMKTS) $248.75 +16.75 (+7.22%))

        deleteList = []
        for item1 in knowledge_panel_page:
            if item1 not in deleteList:
                for item2 in knowledge_panel_page:
                    if item1 != item2 and item2 in knowledge_panel_page[item1]:
                        deleteList.append(item2)
                        continue
        for item in deleteList:
            if (item in knowledge_panel_page):
                del (knowledge_panel_page[item])

        # pagination (Mobile)

        if soup.find('a', attrs={"aria-label": "Next page"}, href=True):
            out_json['pagination']['next'] = 'https://all-serp.com/serp?language=' + language + '&location=' + location + '&search_engine=google&keyword=' + keyword.replace(' ', '+') + '&api_key=' + api_key + '&page=' + str(int(page_limit) + 1)

            for index in range(1, 11):
                if (index == page_limit):
                    continue
                out_json['pagination']['other_pages'].append('https://all-serp.com/serp?language=' + language + '&location=' + location + '&search_engine=google&keyword=' + keyword + '&api_key=' + api_key + '&near=' + near + '&page=' + str(int(index)))

        # pagination 2 (Web)

        if out_json['pagination']['next'] == '' and soup.find('div', attrs={"role": "navigation"}):
            out_json['pagination']['next'] = 'https://all-serp.com/serp?language=' + language + '&location=' + location + '&search_engine=google&keyword=' + keyword.replace(' ', '+') + '&api_key=' + api_key + '&page=' + str(int(page_limit) + 1)

            for index in range(1, 11):
                if (index == page_limit):
                    continue
                out_json['pagination']['other_pages'].append('https://all-serp.com/serp?language=' + language + '&location=' + location + '&search_engine=google&keyword=' + keyword + '&api_key=' + api_key + '&near=' + near + '&page=' + str(int(index)))

        # local_results

        a_div_list = []
        position_local = 1
        for a in soup.findAll('a'):
            if (a.find('div') and a.find('div').find('div') and a.find('div').find('div').find('span') and a.find('div').find('div').find('span').find('h3')):

                json_local_result = {}
                json_local_result['position'] = str(position_local)

                if (a['href']):
                    json_local_result['url_search'] = a['href']

                json_local_result['title'] = a.find('div').find('div').find('span').find('h3').text.strip()

                if (len(a.find('div').find('div').findAll('span')) >= 2):
                    second_span = a.find('div').find('div').findAll('span')[1]

                    if (second_span.find('div') and second_span.find('div').find('span')):
                        div_text = second_span.find('div').text
                        span_text = second_span.find('div').find('span').text

                        json_local_result['contact_info'] = div_text.replace(span_text, '').strip()
                    if (second_span.find('span')):
                        json_local_result['rating'] = second_span.find('span').text.strip()

                local_results.append(json_local_result)
                position_local += 1

        url_results = url_results + url_results_page
        url_results_adv = url_results_adv + url_results_adv_page
        url_results_video = url_results_video + url_results_video_page
        question_list = question_list + question_list_page
        related_search_list = related_search_list + related_search_list_page
        knowledge_panel_list.append(knowledge_panel_page)



    except Exception as e:
        print(colored('keyword : ' + keyword + str(e), 'red'))

        out_json['organic_results'] = url_results
        out_json['ad_results'] = url_results_adv
        out_json['video_results'] = url_results_video
        out_json['related_search'] = related_search_list
        out_json['people_also_asked'] = question_list
        out_json['Knowledge_panel'] = knowledge_panel_list
        out_json['local_results'] = local_results

        return out_json

    out_json['Knowledge_panel'] = knowledge_panel_list
    out_json['organic_results'] = url_results
    out_json['ad_results'] = url_results_adv
    out_json['video_results'] = url_results_video
    out_json['people_also_asked'] = question_list
    out_json['related_search'] = related_search_list
    out_json['local_results'] = local_results

    return out_json

def google_extract_info_maps(html, keyword, language, location, number, page_limit, api_key, near):


    # file_out = open(str(datetime.datetime.now()) + 'test_maps_country.html', 'w')
    # file_out.write(str(html))
    # file_out.close()


    out_json = {}
    result = []

    try:

        ##### break condition
        if ('did not match any documents' in str(html) ):
            # print(colored('did not match any documents', 'red'))

            out_json['maps_results'] = result

            return out_json

        data = re.findall(r'\[\\\\\"https://search.google.com/local/reviews\?placeid(.*?)\[null,null,null,', str(html))
        if len(data) > 0:
            for d in data:
                try:
                    d = d.replace('\\\\\\\\u0026', '&').replace('\\\\\\\\u003d', '=').replace('\\\\",\\\\"', ',').replace(
                        '\\\\",null,\\\\"', ',')
                    d = d.replace('\\\\\"', ',').replace('\\\\n', ',').replace('null', '')
                    d = d.replace(',]', ']').replace('[,', '[').replace('\\xe2', '').replace('\\x82', '').replace('\\xac',
                                                                                                                  '').replace(
                        '\\xe2', '-')
                    d = re.sub(",+", ",", d, 0, re.IGNORECASE | re.VERBOSE | re.MULTILINE)
                    d = d.replace(',]', ']').replace('[,', '[')
                    d = d.replace(',[[[[[2,', '')
                    d = d.replace('\\\\\\\\', '')
                    ##############################################################
                    place_ids = re.findall(r'=(.*)&q=', d)
                    reviews = [x.replace(' reviews', '') for x in re.findall(r'[0-9]+ reviews', d)]
                    reviews_temp = [x.replace('],', '').replace(']', '') for x in re.findall(r'\],[0-9]+.[0-9]+,[0-9]+]', d)]
                    reviews_score = [x.split(',')[0] for x in reviews_temp]
                    if len(reviews_score) > 0:
                        reviews_score = reviews_score[0]
                    else:
                        reviews_score = 'None'
                    reviews_count = [x.split(',')[1] for x in reviews_temp]
                    if len(reviews_count) > 0:
                        reviews_count = reviews_count[0]
                    else:
                        reviews_count = 'None'
                    website_temp = re.findall("((www\.|http://|https://)(www\.)*.*?(?=(www\.|http://|https://|$|,)))", d)
                    if len(website_temp) > 0:
                        website = website_temp[0][0]
                    else:
                        website = 'None'

                    lat_long_temp = re.search(r'\[([\d.-]+),\s*([\d.-]+)\]', d).groups()
                    lat = lat_long_temp[0]
                    long = lat_long_temp[1]

                    d_temp = re.sub(r'(.*):0x', '', d)

                    categories_temp = re.findall(r',\[(.*)\],', d_temp)

                    if len(categories_temp) > 0:
                        category = categories_temp[0]
                    else:
                        category = 'None'

                    name = re.search(r'(.*),\[(.*)\],', d_temp).group(1).split(',')[1]

                    address = re.search(r'\],(.*)', d_temp).group(1).replace(name, ' ').replace(', ', ',').replace(',,', ',')
                    if address[0] == ',':
                        address = address[1:]
                    if address[-1] == ',':
                        address = address[:-1]

                    t_result = {}
                    t_result['google_place_id'] = place_ids[0]
                    t_result['name'] = name
                    t_result['address'] = address
                    t_result['Latitude'] = lat
                    t_result['Longitude'] = long
                    t_result['website'] = website
                    t_result['category'] = category
                    t_result['review_score'] = reviews_score
                    t_result['review_count'] = reviews_count
                    # name_ = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode("utf-8")
                    # name_ = name_.replace('\\', '\\\\')

                    tel_temp = re.findall(rf'{re.escape(name)}(.*)tel:(.*){re.escape(name)}', str(html))
                    tel = 'None'
                    if len(tel_temp) > 0:
                        tel_temp = tel_temp[0][0]
                        tel_ = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tel_temp)

                        for te in tel_:
                            if '+' in te:
                                tel = te
                                break

                    t_result['phone'] = tel
                    result.append(t_result)

                except Exception as e:
                    print(e)
                    continue
        else:
            data = re.findall(r'https://www.google.com/search\?q(.*?),\[\\\"https://', str(html))
            for index in range(len((data))):
                try:
                    d = data[index]
                    d = d.replace('\\\\\\\\u0026', '&').replace('\\\\\\\\u003d', '=').replace('\\\\",\\\\"', ',').replace(
                        '\\\\",null,\\\\"', ',')
                    d = d.replace('\\\\\"', ',').replace('\\\\n', ',').replace('null', '')
                    d = d.replace(',]', ']').replace('[,', '[').replace('\\xe2', '').replace('\\x82', '').replace('\\xac',
                                                                                                                  '').replace(
                        '\\xe2', '-')
                    d = re.sub(",+", ",", d, 0, re.IGNORECASE | re.VERBOSE | re.MULTILINE)
                    d = d.replace(',]', ']').replace('[,', '[')
                    d = d.replace(',[[[[[2,', '')
                    d = d.replace('\\\\\\\\', '')

                    d_temp = re.sub(r'(.*):0x', '', d)

                    t_result = {}
                    address = None
                    name = None

                    if (len(re.findall(',\[\[\[\d,\[\[\\\\\"(.*?)\\\\\"\]', d)) > 0):
                        name = re.findall(',\[\[\[\d,\[\[\\\\\"(.*?)\\\\\"\]', d)[0].replace('\(', '').replace('\)', '').replace('\]', '').replace('\[', '')
                        if (len(name) >= 3 and len(re.findall(f'{name[-3:]},(.*?)\\\\"\]', d)) > 0):
                            address = re.findall(f'{name[-3:]},(.*?)\\\\"\]', d)[0]
                    t_result['address'] = address
                    t_result['name'] = name

                    tel_temp = re.findall(rf'{re.escape(name)}(.*)tel:(.*){re.escape(name)}', str(html))
                    tel = 'None'
                    if len(tel_temp) > 0:
                        tel_temp = tel_temp[0][0]
                        tel_ = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tel_temp)

                        for te in tel_:
                            if '+' in te:
                                tel = te
                                break
                    t_result['phone'] = tel

                    website_temp = re.findall("((www\.|http://|https://)(www\.)*.*?(?=(www\.|http://|https://|$|,)))", d)
                    website = 'None'

                    if len(website_temp) > 0:
                        website_list = website_temp[0]
                        for item in website_list:
                            if ('google' not in item and item != 'https://' and item != 'http://' and ('.' in item)):
                                website = item
                                break

                    t_result['website'] = website

                    categories_temp = re.findall(r',\[(.*)\],', d_temp)

                    if len(categories_temp) > 0:
                        category = categories_temp[0]
                    else:
                        category = 'None'
                    t_result['category'] = category

                    lat = None
                    long = None
                    if (re.search(r'\[([\d.-]+),\s*([\d.-]+)\]', d)):
                        lat_long_temp = re.search(r'\[([\d.-]+),\s*([\d.-]+)\]', d).groups()
                        if (len(lat_long_temp) == 2 and '.' in lat_long_temp[0] and '.' in lat_long_temp[1]):
                            lat = lat_long_temp[0]
                            long = lat_long_temp[1]

                    t_result['Latitude'] = lat
                    t_result['Longitude'] = long

                    reviews = [x.replace(' reviews', '') for x in re.findall(r'[0-9]+ reviews', d)]
                    reviews_temp = [x.replace('],', '').replace(']', '') for x in re.findall(r'\],[0-9]+.[0-9]+,[0-9]+]', d)]
                    reviews_score_list = [x.split(',')[0] for x in reviews_temp]
                    reviews_score = None
                    reviews_count = None

                    if len(reviews_score_list) > 0:
                        reviews_score = reviews_score[0]
                    else:
                        reviews_score = 'None'

                    try:
                        reviews_count = [x.split(',')[1] for x in reviews_temp]
                        if (reviews_count == []):
                            reviews_count = None
                    except Exception as e:
                        pass

                    t_result['review_score'] = reviews_score
                    t_result['review_count'] = reviews_count

                    result.append(t_result)
                except Exception as e:
                    # print(e)

                    continue

                ##############################################################

    except Exception as e:
        print(colored('keyword : ' + keyword + ' >>> ' + str(e), 'red'))

        out_json['maps_results'] = result

        return out_json

    out_json['maps_results'] = result


    return out_json

def check_knowledge_panel_website (knowledge_panel_list, companyName):

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



    if Website == None or Website == '':
        return Website
    else:
        return Website

def get_first_valid_list(input_list, companyName):

    out_set = []

    if (len(input_list) ==0):
        return out_set

    for i in range(len(input_list)):
        if (i > 2):
            return out_set
        # print (colored(input_list[i]['url'],'yellow'))
        main_url = get_main_part_website(input_list[i]['url'])
        # if (find_in_socialmedia(main_url)):
        #     continue
        # if (not notExistInBasicSites_db(input_list[i]['url'])):
        #     continue
        # if ('/company/' in input_list[i]['url'] or '/companies/' in input_list[i]['url']):
        #     continue
        if (False):
            continue
        else :

            set_json = {}
            set_json['input_url'] = input_list[i]['url']
            set_json['main_url'] = get_main_part_website(input_list[i]['url'])
            set_json['title'] = input_list[i]['title']
            out_set.append(set_json)

        return out_set

    return out_set

def get_valid_list(input_list, companyName):

    out_set = []

    if (len(input_list) ==0):
        return out_set

    for i in range(len(input_list)):
        if (len(out_set) == 3):
            return out_set

        set_json = {}
        set_json['input_url'] = input_list[i]['url']
        set_json['main_url'] = get_main_part_website(input_list[i]['url'])
        set_json['title'] = input_list[i]['title']
        out_set.append(set_json)


    return out_set

def select_valid_url(input_url, search_list, companyName, index):
    out_list = []

    if (input_url[-1] == '/'):
        input_url = input_url[0:-1]
    input_url = input_url.replace('www.','').replace('http://','').replace('https://','')

    item_list = input_url.split('/')
    if (len(item_list) == 1):
        out_list.append(search_list[index]['input_url'])
        return out_list
    if (len(item_list) == 2):
        second_item = item_list[1].strip().lower()

        if ('/en/' in input_url or 'en-' in input_url or '_en' in input_url or second_item.startswith('#') or 'home' in second_item or 'index' in second_item or'contact' in second_item or 'about' in second_item or second_item in country_list or second_item in country_code_list or second_item in language_2digits_list or second_item in language_3digits_list):
            out_list.append(search_list[index]['input_url'])
            return out_list
    elif (len(item_list) > 2):
        domain_split_list = item_list[0].split('.')
        domain = ''
        for i in range(len(domain_split_list)-1):
            if (i==len(domain_split_list)-2):
                domain += domain_split_list[i]
            else:
                domain += domain_split_list[i] + '.'

        first_item = domain.strip().replace('-', '')
        if ((('/en/' in input_url or 'en-' in input_url or '_en' in input_url) and len(item_list) == 3 ) or (first_item.lower() in companyName.replace(' ','').replace('-', '').lower())):
            out_list.append(search_list[index]['input_url'])
            return out_list
    return out_list

def select_module_slash_based(search_list, companyName):

    out_list = []

    if (search_list ==[]):
        return out_list

    if (len(out_list) ==0 and len(search_list) > 0 ):
        for index, item in enumerate(search_list):
            selected_website_second = item['input_url']

            if (find_in_socialmedia(selected_website_second)):
                continue
            else:
                out_list_level= select_valid_url(selected_website_second, search_list, companyName, index)
                if (len(out_list_level) > 0):
                    for website in out_list_level:
                        out_list.append(website)


    return out_list

def get_main_part_website(input_url):

    return input_url

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

def google_tor( keyword):

    cnt = 1
    while True:
        try:

            with tor_requests_session() as s:

                google_url = 'https://www.google.com/search?q=' + str(keyword).replace(' ', '+') + '&hl=en&gl=us&source=web'

                html = s.get(google_url, timeout = 10)


                if (html.status_code == 200):
                    # print(colored('Open Google Search Results Successfully...', 'green'))
                    return html

                else:
                    continue


        except Exception as e:
            continue

def crawl_page_tor(url):

    while True:
        try:

            with tor_requests_session() as s:


                html = s.get(url, timeout=10)

                if (html.status_code == 200):
                    return html

                else:
                    continue

        except Exception as e:
            continue

def get_page_html(inputURL):

    if ('http' not in inputURL):
        inputURL = 'https://' + inputURL

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    s = requests.session()



    html = ''

    selectedURL = inputURL.strip()

    attempt_limit = 3
    attempt = 0


    while True and attempt <= attempt_limit:

        # headers['User-Agent'] = useragent
        try:
            attempt += 1

            if attempt == 1:
                html = s.get(str(selectedURL), headers=headers, timeout = 20, verify=False)
            else:
                proxy, useragent = change_proxy_bank()
                html = s.get(str(selectedURL), proxies={'http': proxy, 'https': proxy}, headers=headers, timeout = 20, verify=False)

            # html = s.get(str(selectedURL), headers=headers, timeout=20, allow_redirects=True)

            if (html.status_code == 404):

                # os.environ['http_proxy'] = ''
                # os.environ['https_proxy'] = ''
                # os.environ['HTTP_PROXY'] = ''
                # os.environ['HTTPS_PROXY'] = ''
                print(colored('404 Error occured !', 'red'))
                s.close()
                # s = requests.session()
                # proxy, useragent = change_proxy()
                continue

            if (html.status_code == 403):
                print (colored('403 Error occured !','red'))
                s.close()
                s= requests.session()

                # os.environ['http_proxy'] = ''
                # os.environ['https_proxy'] = ''
                # os.environ['HTTP_PROXY'] = ''
                # os.environ['HTTPS_PROXY'] = ''
                # proxy, useragent = change_proxy()
                continue

            # html = str(html.content)



        except Exception as e:
            # print( '2'+str(e))
            print(e)
            s.close()
            s = requests.session()

            continue
        else:
            break

    print(colored('get html of page ' + str(inputURL) , 'green'))
    return html

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

def cuf_tor(html, keyword):


    companyName = keyword

    out_result = google_extract_info(html, keyword, 'en', 'united states', 10, 1, 'api_key', 'usa')
    KPs = out_result['Knowledge_panel']
    google_organic_results = out_result['organic_results']

    print (colored('==================================== Weighting ==========================================','magenta'))


    selected_website_google_list = get_valid_top_list(google_organic_results) # return top 4 organic urls
    selected_website_list = select_module_slash_social(selected_website_google_list, companyName)

    ####

    json_out = {}
    json_out['query'] = companyName
    json_out['url'] = 'Not Found'


    for item in selected_website_list:
        json_out['url'] = get_main_part_website(item)
        break # only return one value


    return (json_out)

    
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

def sb_tor(html, keyword, social_network):


    companyName = keyword

    out_result = google_extract_info(html, keyword, 'en', 'united states', 10, 1, 'api_key', 'usa')
    KPs = out_result['Knowledge_panel']
    google_organic_results = out_result['organic_results']

    print (colored('==================================== Weighting ==========================================','magenta'))

    weighted_list = weight_search_engine_output_social_network(google_organic_results, companyName, social_network)
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

        break  # only return one value

    # add_mongodb_social_network(companyName, json_out, social_network)
    print(colored('company_name : ' + companyName + ' and ' + social_network + '_profile : ' + str(selected_website[0]) + ' added to mongodb !', 'cyan'))

    return (json_out)



def linkedin_tor(html, keyword):

    companyName = keyword

    out_result = google_extract_info(html, keyword, 'en', 'united states', 10, 1, 'api_key', 'usa')
    KPs = out_result['Knowledge_panel']
    google_organic_results = out_result['organic_results']

    print(colored('==================================== Linkedin Weighting ==========================================', 'magenta'))

    weighted_list = weight_search_engine_output_linkedin(google_organic_results, companyName)
    selected_website = weighted_list

    json_out = {}

    if (selected_website == 'Search list is empty !!!' or len(selected_website) == 0):

        json_out['query'] = companyName
        json_out['url'] = 'Not Found'


        return (json_out)

    list_out = []

    for item in selected_website:
        json_out['query'] = companyName
        json_out['url'] = item


        break # only return one value
    return json_out

def extract_all(company_website):


    all_link_extracted = extract_all_links_from_url_init(company_website)
    if (len(all_link_extracted) > 10):
        all_link_extracted = all_link_extracted[0:10]

    list_email, list_phone, list_whatsapp, list_social = all_info_parse_multi_process(0, all_link_extracted, 'all', company_website)
    email_result = clear_emailList(set(list_email), company_website)
    phone_result = clear_phoneList(set(list_phone), company_website)
    linkedin = 'Not Found'
    for link in list_social:
        if ('linkedin_profile' in link):
            linkedin = link['linkedin_profile']
            break
    return linkedin, phone_result, email_result

def dtc_tor(html):

    result_json = {'company_name': 'Not Found'}
    try:
        if (len(html) > CHAR_HTML_LIMIT):
            return result_json
        content = html
        soup = BeautifulSoup(content, 'html.parser')
        if (soup.find('title')):
            result = soup.find('title').text.strip()
            result = result.split(' - ')[0].split(' – ')[0].split(' _ ')[0].split(' __ ')[0].split(' : ')[0].split(' . ')[0].split(' · ')[0].split(' * ')[0].split(' | ')[0].split(' ~ ')[0].split(' > ')[0].split(' < ')[0].split(' » ')[0].split(' « ')[0]

            result_json = {'company_name': result.strip()}

    except Exception as e:
        print(e)

    return result_json


def extract_all_links_html(html, selectedURL):


    outList=[]

    outList.append(selectedURL)

    try:
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        # links = [a.get('href') for a in soup.find_all('a', href=True)]
        li_list = soup.find_all('li')
        links = set()
        for li in li_list:
            if (li.find('a') and li.find('a').get("href") \
                    and ('contact' in str(li.find('a')) or 'Contact' in str(li.find('a')) \
                         or 'connect' in str(li.find('a')) or 'Connect' in str(li.find('a')) \
                         or 'about' in str(li.find('a')) or 'About' in str(li.find('a')))):
                # or 'product' in str(li.find('a')) or 'Product' in str(li.find('a')) \
                # or 'service' in str(li.find('a')) or 'Service' in str(li.find('a')))):
                links.add(li.find('a')['href'])
                # if ('http://' in li.find('a')['href'] or 'https://' in li.find('a')['href']):
                #     links.add(li.find('a')['href'])
                # else:
                #     links.add(urljoin('http:', li.find('a')['href']).replace('///', '//'))
                # a =2

        mainPartURL = tldextract.extract(selectedURL).domain

        for link in links:

            urlValidLink = link

            if (selectedURL not in link or link.startswith('/')):
                urlValidLink = urljoin(selectedURL, link).replace('///', '//')
            if ('http://' not in urlValidLink and 'https://' not in urlValidLink):
                urlValidLink = urljoin('http:', urlValidLink).replace('///', '//')

            # if (not validators.url(urlValidLink) or check_file_extention(urlValidLink)):
            if (check_file_extention(urlValidLink)):
                continue

            if ((not find_in_socialmedia(urlValidLink)) and mainPartURL in urlValidLink):
                outList.append(urlValidLink.strip())

    except Exception as e:
        print(e)

    return outList

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

def weight_search_engine_output_linkedin(out_result_google_company, companyName):

    google_res_company = out_result_google_company
    google_set_company = get_set_list_linkedin(google_res_company, companyName)
    return google_set_company

def get_set_list_linkedin(input_list, companyName):

    out_set = []

    if (input_list == None or len(input_list) == 0 ):
        return out_set

    item = input_list[0]
    main_part = yarl.URL(get_main_part_website_socialnetwork(item['url']).replace('//', '').replace('www.', '')).path
    if ('linkedin.com/company/' not in item['url']):
        return out_set

    companyName_tokens = companyName.split(' ')
    len_total = len(companyName_tokens)
    token_passed = 0

    for token in companyName_tokens:
        if token.strip().lower() in item['title'].replace(' ','').lower():
            token_passed += 1
    if (token_passed >= 2 or token_passed/len_total > 0.5):
        # set_json = {}
        # set_json['input_url'] = item['url']
        # set_json['main_url'] = get_main_part_website_linkedin(item['url'])
        # set_json['title'] = item['title']
        # out_set.append(set_json)
        out_set.append(item['url'].split('&')[0])

    return out_set

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

def maps_tor(html, keyword):

    json_out = {}
    json_out['query'] = keyword
    json_out['url'] = 'Not Found'

    out_result = google_extract_info_maps(html, keyword, 'en', 'united states', 10, 1, 'api_key', 'usa')

    for item in out_result['maps_results']:
        if (keyword.replace(' ','').lower() in item['name'].replace(' ','').lower()):
            if (item['website'] != None and item['website'] != 'None'):
                json_out['url'] = item['website']
                break

    return json_out

def check_file_extention (inputUrl):

    if ('.mp3' in str(inputUrl).lower()):
        return True
    if ('.jpg' in str(inputUrl).lower()):
        return True
    if ('.jpeg' in str(inputUrl).lower()):
        return True
    if ('.gif' in str(inputUrl).lower()):
        return True
    if ('.png' in str(inputUrl).lower()):
        return True
    if ('.ico' in str(inputUrl).lower()):
        return True
    if ('.jpx' in str(inputUrl).lower()):
        return True
    if ('.bmp' in str(inputUrl).lower()):
        return True
    if ('.psd' in str(inputUrl).lower()):
        return True

    if ('.avi' in str(inputUrl).lower()):
        return True
    if ('.mp4' in str(inputUrl).lower()):
        return True

    if ('.tar' in str(inputUrl).lower()):
        return True
    if ('.zip' in str(inputUrl).lower()):
        return True
    if ('.gz' in str(inputUrl).lower()):
        return True
    if ('.mpg' in str(inputUrl).lower()):
        return True
    if ('.flv' in str(inputUrl).lower()):
        return True

    if ('.pdf' in str(inputUrl).lower()):
        return True

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

def extract_all_links_from_url_init(inputURL):


    if ('http' not in inputURL):
        inputURL = 'https://' + inputURL

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    s = requests.session()



    outList = []

    outList.append(inputURL.strip())
    selectedURL = inputURL.strip()

    attempt_limit = 3
    attempt = 0

    while attempt <= attempt_limit:

        # headers['User-Agent'] = useragent
        try:
            print(colored('TRY ++++++++++++++++++++++ '+ str(attempt), 'yellow'))
            attempt += 1

            if attempt == 1:
                html = s.get(str(selectedURL), headers=headers, timeout=20, verify=False)
            else:
                proxy, useragent = change_proxy_bank()
                # os.environ['http_proxy'] = proxy
                # os.environ['https_proxy'] = proxy
                # os.environ['HTTP_PROXY'] = proxy
                # os.environ['HTTPS_PROXY'] = proxy
                html = s.get(str(selectedURL), proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=20, verify=False)
                # html = s.get(str(selectedURL), headers=headers, timeout=20, allow_redirects=True, verify=False)


            # html = s.get(str(selectedURL), headers=headers, timeout=20, allow_redirects=True)

            if (html.status_code == 404):

                # os.environ['http_proxy'] = ''
                # os.environ['https_proxy'] = ''
                # os.environ['HTTP_PROXY'] = ''
                # os.environ['HTTPS_PROXY'] = ''
                print(colored('404 Error occured !', 'red'))
                s.close()
                s = requests.session()
                # proxy, useragent = change_proxy()
                continue

            if (html.status_code == 403):
                print (colored('403 Error occured !','red'))
                s.close()
                s= requests.session()

                # os.environ['http_proxy'] = ''
                # os.environ['https_proxy'] = ''
                # os.environ['HTTP_PROXY'] = ''
                # os.environ['HTTPS_PROXY'] = ''
                # proxy, useragent = change_proxy()
                continue

            html = html.content
            soup = BeautifulSoup(html, 'html.parser')
            # links = [a.get('href') for a in soup.find_all('a', href=True)]
            li_list = soup.find_all('li')
            links = set()
            for li in li_list:
                if (li.find('a') and li.find('a').get("href") \
                        and ('contact' in str(li.find('a')) or 'Contact' in str(li.find('a')) \
                        or 'connect' in str(li.find('a')) or 'Connect' in str(li.find('a')) \
                        or 'about' in str(li.find('a')) or 'About' in str(li.find('a')))):
                        # or 'product' in str(li.find('a')) or 'Product' in str(li.find('a')) \
                        # or 'service' in str(li.find('a')) or 'Service' in str(li.find('a')))):
                    links.add(li.find('a')['href'])
                    # if ('http://' in li.find('a')['href'] or 'https://' in li.find('a')['href']):
                    #     links.add(li.find('a')['href'])
                    # else:
                    #     links.add(urljoin('http:', li.find('a')['href']).replace('///', '//'))
                    # a =2


            mainPartURL = tldextract.extract(selectedURL).domain


            for link in links:

                urlValidLink = link

                if (selectedURL not in link or link.startswith('/')):
                    urlValidLink = urljoin(selectedURL, link).replace('///','//')
                if ('http://' not in urlValidLink  and 'https://' not in urlValidLink):
                    urlValidLink = urljoin('http:', urlValidLink).replace('///', '//')



                # if (not validators.url(urlValidLink) or check_file_extention(urlValidLink)):
                if (check_file_extention(urlValidLink)):
                    continue


                if ((not find_in_socialmedia(urlValidLink)) and mainPartURL in urlValidLink):

                    outList.append(urlValidLink.strip())

            # a =2
            # return [selectedURL]
            break


        except Exception as e:
            # print( '2'+str(e))
            print(e)
            s.close()
            s = requests.session()
            # os.environ['http_proxy'] = ''
            # os.environ['https_proxy'] = ''
            # os.environ['HTTP_PROXY'] = ''
            # os.environ['HTTPS_PROXY'] = ''
            #
            # proxy, useragent = change_proxy()

            # os.environ['http_proxy'] = proxy
            # os.environ['HTTP_PROXY'] = proxy
            # os.environ['https_proxy'] = proxy
            # os.environ['HTTPS_PROXY'] = proxy

            continue


    print(colored('all links ( '+ str(len(outList)) +' links) extracted from page : ' , 'green') + colored(inputURL,'magenta'))
    return outList

def extract_email_from_body(body, domain, id):

    modify_email_html_string = modify_string_for_email(str(body))
    commonRegexEmailList = set(commonregex.email.findall(modify_email_html_string))
    emailList = clear_emailList_allserp(commonRegexEmailList, domain, id)
    return emailList

def extract_phone_from_body(body):

    modify_phone_html_string = modify_string_for_phone(str(body))
    commonRegexPhoneList = set(commonregex.phone.findall(modify_phone_html_string))
    phoneList = clear_phoneList(commonRegexPhoneList, '')
    return phoneList

def extract_allserp_email_info(inputList, domain, id):

    emailList = []
    whatsappList = []
    phoneList = []

    for item in inputList:
        if 'body' in item:
            body = item['body']
            emailList_item = extract_email_from_body(body,domain,id)
            if (len(emailList_item) > 0):
                phoneList_item = extract_phone_from_body(body)
                if ('whatsapp' in body.lower()):
                    for phone in phoneList_item:
                        whatsappList.append(phone)
                else:
                    for phone in phoneList_item:
                        phoneList.append(phone)

                for email in emailList_item:
                    emailList.append(email)

    return list(set(emailList)), list(set(whatsappList)), list(set(phoneList))

def search_mail_module(id, domain):



    #print(colored('email search by Allsepr called for : ' + '"email: ' + id + '@' + domain+ '"', 'blue'))

    # google_result = google_search('"email: ' + id + ' ' + domain+ '"')
    # allserp_html = google_tor(id + domain + ' email').text

    allserp_html = open('allserp_amootiranian.html', 'r').read()
    google_result = google_extract_info(allserp_html, id + domain + ' email', 'en', 'us', 10, 1, 'api_key', 'usa')['organic_results']

    emailList, whatsappList, phoneList = extract_allserp_email_info(google_result, domain, id)

    print(colored('extracted information email_list : ' + str(emailList) + ', phone_list : ' + str(phoneList) + ', whatsapp_list : ' + str(whatsappList), 'green'))


    return emailList,whatsappList,phoneList

def get_email_phone_from_allserp(company_website):

    try:


        domain = company_website.replace('www.','').replace('http://','').replace('https://','')
        id = '*'

        print(colored('send email_from_allserp API request for domain :' + domain + ', and id :' + id , 'blue'))


        emailList, whatsappList, phoneList = search_mail_module(id, domain)
        return emailList, whatsappList, phoneList

    except Exception as e:
        print(e)
        return [], [], []

def all_info_parse_multi_process ( process , links, mode, company_website):

    ###############################################################################
    list_general_phone, list_general_email, list_general_social = [], [], []
    for i in range(len(links)):
        phone_list, email_list, social_list = info_parse(i, links[i], mode, len(links))
        list_general_phone = list_general_phone + phone_list
        list_general_email = list_general_email + email_list
        list_general_social = list_general_social + social_list

    list_general_whatsapp = []

    return list_general_email, list_general_phone, list_general_whatsapp, list_general_social

def cleanMe(html):
    if (len(html) > 1000000):
        return ''

    soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def modify_string_for_phone (input_string):
    return input_string.replace(' ( ', '').replace(' ) ', '').replace(' (', '').replace(') ', '').replace('-', '')

def modify_string_for_email (input_string):
    return input_string.replace('(at)', '@') \
                       .replace('( at )', '@') \
                       .replace('[at]', '@') \
                       .replace('[ at ]', '@') \
                       .replace('{at}', '@') \
                       .replace('{ at }', '@') \
                       .replace('(dot)', '.') \
                       .replace('( dot )', '.') \
                       .replace('[dot]', '.') \
                       .replace('[ dot ]', '.') \
                       .replace('{dot}', '.') \
                       .replace('\\n', ' ') \
                       .replace('{ dot }', '.')\
                       .replace('u003e', ' ')

def info_parse ( process , link, mode, total_count):


    list_phone = []
    list_social = []
    list_email = []
    json_social = {}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    # proxy, useragent = change_proxy()

    cnt_ = 0


    commonRegexPhoneList = []
    commonRegexEmailList = []
    print('process: ' + colored(str(process+1) + ' / ' + str(total_count), 'green') + colored( ' link extracting from  url : ' + link, 'magenta'))


    try_attempt = 1


    # html = crawl_page_tor(link)

    while (try_attempt <= 1):

        try:
            try_attempt += 1
            html = get_page_html(link)
            if html == '':
                continue

            html_content_raw = html.content
            soup = BeautifulSoup(html_content_raw, 'html.parser')

            # cleaner = Cleaner(page_structure=False)
            # clean_html = cleaner.clean_html(str(html_content_raw))
            clean_html = cleanMe(html_content_raw)
            html_content = BeautifulSoup(clean_html,'html.parser').text

            ##############################################################################
            if mode == 'phone' or mode == 'all':
                modify_phone_html_string = modify_string_for_phone(str(html_content))

                # commonRegexPhoneList = set(commonregex.phone.findall(modify_phone_html_string))
                commonRegexPhoneList = set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', modify_phone_html_string))

            if mode == 'email' or mode == 'all':
                modify_email_html_string = modify_string_for_email(str(html_content_raw))
                commonRegexEmailList = set(commonregex.email.findall(modify_email_html_string))

            if mode == 'all':

                a_list = soup.find_all('a', href= True)


                for a in a_list:
                    if ('facebook.com/' in a['href']):
                        json_social['facebook_profile'] = a['href']
                    elif ('instagram.com/' in a['href']):
                        json_social['instagram_profile'] = a['href']
                    elif ('linkedin.com/company/' in a['href']):
                        json_social['linkedin_profile'] = a['href']
                    elif ('twitter.com/' in a['href']):
                        json_social['twitter_profile'] = a['href']
                    elif ('youtube.com/' in a['href']):
                        json_social['youtube_profile'] = a['href']





            ##############################################################################

        except Exception as e:

            print(colored(str(e),'red'))
            continue
        else:
            break

    if mode == 'phone' or mode == 'all':
        for item in list(commonRegexPhoneList):
            list_phone.append(item)
    if mode == 'email' or mode == 'all':
        for item in list(commonRegexEmailList):
            list_email.append(item)
    if mode == 'all':
        list_social.append(json_social)


    return list_phone, list_email, list_social

def info_parse_html(link, html, mode):

    list_phone = []
    list_email = []
    list_social = []
    commonRegexPhoneList = set()
    commonRegexEmailList = set()

    json_social={}

    try:

        if html == '':
            return list_phone, list_email, list_social


        html_content_raw = html.content
        soup = BeautifulSoup(html_content_raw, 'html.parser')

        # cleaner = Cleaner(page_structure=False)
        # clean_html = cleaner.clean_html(str(html_content_raw))
        clean_html = cleanMe(html_content_raw)

        html_content = BeautifulSoup(clean_html, 'html.parser').text

        ##############################################################################
        if mode == 'phone' or mode == 'all':
            modify_phone_html_string = modify_string_for_phone(str(html_content))

            # commonRegexPhoneList = set(commonregex.phone.findall(modify_phone_html_string))
            commonRegexPhoneList = set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', modify_phone_html_string))

        if mode == 'email' or mode == 'all':
            modify_email_html_string = modify_string_for_email(str(html_content_raw))
            commonRegexEmailList = set(commonregex.email.findall(modify_email_html_string))

        if mode == 'all':

            a_list = soup.find_all('a', href=True)

            for a in a_list:
                if ('facebook.com/' in a['href']):
                    json_social['facebook_profile'] = a['href']
                elif ('instagram.com/' in a['href']):
                    json_social['instagram_profile'] = a['href']
                elif ('linkedin.com/company/' in a['href']):
                    json_social['linkedin_profile'] = a['href']
                elif ('twitter.com/' in a['href']):
                    json_social['twitter_profile'] = a['href']
                elif ('youtube.com/' in a['href']):
                    json_social['youtube_profile'] = a['href']
    except Exception as e:

        print(e)

    if mode == 'phone' or mode == 'all':
        for item in list(commonRegexPhoneList):
            list_phone.append(item)
    if mode == 'email' or mode == 'all':
        for item in list(commonRegexEmailList):
            list_email.append(item)
    if mode == 'all':
        list_social.append(json_social)

    list_phone = clear_phoneList(list_phone, link)
    list_email = clear_emailList(list_email, link)


    return list_phone, list_email, list_social

def clear_emailList_allserp (inputEmailList, domain, id):

    id_clear = id.replace('*','').strip()

    outEmailList_phase1 = set()
    outEmailList_phase2 = set()

    for email in inputEmailList:
        #print(str(i) + ' from ' + str(len(inputEmailList)))
        try:
            # if validate_email(email) and re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
            if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email.lower()):
                    outEmailList_phase1.add(email.lower())

        except Exception as e:
            print (e)
            continue

    for email in outEmailList_phase1:

        website_host = domain.strip().lower()
        if website_host != '' and website_host not in email: # ensnure domain is in email
            continue
        if (id_clear != '' and id_clear.lower() not in email): # ensure id is in email with exception *
            continue
        if (email.startswith('email@') or email.startswith('last@') or email.startswith('first@') or\
                    ('first' in email and 'name' in email) or ('last' in email and 'last' in email) or\
                    ('john' in email and 'smith' in email) or email.startswith('j_smith@')):
            continue

        outEmailList_phase2.add(email)


    return set(list(outEmailList_phase2))

def clear_emailList (inputEmailList, inputURL):
    outEmailList_phase1 = []
    outEmailList_phase2 = []

    website_domain = tldextract.extract(inputURL).domain

    for email in inputEmailList:
        #print(str(i) + ' from ' + str(len(inputEmailList)))
        try:
            # if validate_email(email) and re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):

            if ('@' not in email or (website_domain not in email.split('@')[-1])):

                continue

            if ('/' in email or '.png' in email or email.startswith('you@') or email.startswith('email@') or email.startswith('last@') or email.startswith('first@') or \
                    ('first' in email and 'name' in email) or ('last' in email and 'last' in email) or \
                    ('john' in email and 'smith' in email) or email.startswith('j_smith@') or 'xx' in email or 'XX' in email \
                    or 'anonymous' in email or 'noreply' in email or 'no_reply' in email or 'example.com' in email):
                continue

            if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email.lower()):
                print(colored(email, 'yellow'))
                if (email.lower() not in outEmailList_phase1):
                    outEmailList_phase1.append(email.lower())

        except Exception as e:
            continue


    for email in outEmailList_phase1:
        try:
            # website_host = yarl.URL(inputURL).host.replace('http://', '').replace('https://', '').replace('www.', '').replace('.com', '').replace('.net', '').replace('.org', '')  # get the host part of webstie in order to ensure links are the same host with input url
            website_host = ''

            website_host = tldextract.extract(inputURL).domain


            if website_host != '' and website_host != None and website_host not in email:
                continue
            if ('u003e' in email):
                email = email.replace('u003e', '')

            if (email.lower() not in outEmailList_phase2):
                outEmailList_phase2.append(email.lower())
        except Exception as e:
            continue

    # if (len(outEmailList_phase2) ==0):
    #     outEmailList_phase2 = outEmailList_phase1

    return outEmailList_phase2

def clear_phoneList (inputPhoneList, url):
    outPhoneList = set()
    for phone in inputPhoneList:
        try:
            phone_edited = phone.replace('-','').replace(')','').replace('(','').replace(' ','')
            if (not phone_edited.startswith('+')):
                phone_edited = '+' + phone_edited
            if ('contact' in url or 'Contact' in url):
                outPhoneList.add(phone_edited)
            elif phonenumbers.is_valid_number(phonenumbers.parse(phone_edited, None)) and '.' not in phone_edited:
                outPhoneList.add(phone_edited)
        except:
            continue
    return list(outPhoneList)

def get_country_list (phoneList):
    if (phoneList ==  ['Not Found']):
        return []
    if phoneList == None:
        return []
    if len(phoneList) == 0:
        return []

    countryList = get_countries(phoneList)
    return countryList

def get_countries(phonenumbers):
    locations = []
    for phone in phonenumbers:
        try:
            locations.append(pycountry.countries.get(alpha_2=phone_country(phone)).official_name)
        except Exception as e:
            locations.append('Not Found')

    result=[]
    for i in range(len(locations)):
        res_={}
        res_[phonenumbers[i]] = locations[i]
        result.append(res_)

    return result

def email_phone_social (input_url):


    jsonLoaded= {}

    all_link_extracted = extract_all_links_from_url_init(input_url)

    # emailListGlobal = all_info_parse(0, all_link_extracted, 'email')
    list_email, list_phone, list_whatsapp, list_social = all_info_parse_multi_process(0, all_link_extracted, 'all', input_url)

    # jsonLoaded['emailList'] = clear_emailList(set(emailListGlobal), companyWebsite)
    email_final = clear_emailList(set(list_email), input_url)
    jsonLoaded['emailList'] = email_final

    phone_final = clear_phoneList(set(list_phone), input_url)
    jsonLoaded['phoneList'] = phone_final

    whatsapp_final= clear_phoneList(set(list_whatsapp), input_url)
    jsonLoaded['whatsapp_list'] = whatsapp_final

    # jsonLoaded_phone['countryList'] = get_country_list(jsonLoaded_phone['phoneList'])
    if (len(list_social) > 0):
        jsonLoaded['social_network'] = list_social[0]
    else:
        jsonLoaded['social_network'] = ['Not Found']



    if (len(jsonLoaded['emailList']) == 0):
        jsonLoaded['emailList'] = ['Not Found']

    if (len(jsonLoaded['phoneList']) == 0):
        jsonLoaded['phoneList'] = ['Not Found']

    if (len(jsonLoaded['whatsapp_list']) == 0):
        jsonLoaded['whatsapp_list'] = ['Not Found']

    jsonLoaded['query'] = input_url



    country_list = get_country_list(jsonLoaded['phoneList'])

    print(colored('total email extracted : '+ str(len(jsonLoaded['emailList'])) + ' from page : ','green' ) + input_url)
    print(colored('total phone extracted : '+ str(len(jsonLoaded['phoneList'])) + ' from page : ','green' ) + input_url)
    print(colored('total whatsapp extracted : '+ str(len(jsonLoaded['whatsapp_list'])) + ' from page : ','green' ) + input_url)
    print(colored('total social_network extracted : '+ str(len(jsonLoaded['social_network'])) + ' from page : ','green' ) + input_url)

    jsonLoaded['countryList'] = get_country_list(jsonLoaded['phoneList'])

    return jsonLoaded


