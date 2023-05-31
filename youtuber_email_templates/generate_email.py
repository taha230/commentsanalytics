from pymongo import MongoClient
import pymongo
import warnings
from termcolor import colored
warnings.filterwarnings('ignore')
from bson.objectid import ObjectId
from multiprocessing import Manager
import multiprocessing
import pymongo
from difflib import SequenceMatcher
import time
import tldextract



input_email_file = open('youtuber_email_templates/input_info.txt', 'r')
input_content = input_email_file.readlines()

output_email_file = open('youtuber_email_templates/email_template.txt', 'w')

youtube_channel_name = input_content[1].strip().title()
youtube_video_title = input_content[2].strip().title()
youtube_video_url = input_content[3].strip()

positive_percent = int(input_content[4].strip())
neutral_percent = int(input_content[5].strip())
negative_percent = int(input_content[6].strip())

dominant_sentiment = 'Positive'
dominant_tag = 'Great !!! 🎉'

if (neutral_percent > positive_percent and neutral_percent > negative_percent):
    dominant_sentiment = 'Neutral'
    dominant_tag = 'Good !!! 💪'
    
if (negative_percent > positive_percent and negative_percent > neutral_percent):
    dominant_sentiment = 'Negative'
    dominant_tag = 'Not Bad !!! 😐'


keyword1_name = input_content[7].split(',')[0].strip()
keyword1_count = input_content[7].split(',')[1].strip()
keyword1_positive_percent = input_content[7].split(',')[2].strip()

keyword2_name = input_content[8].split(',')[0].strip()
keyword2_count = input_content[8].split(',')[1].strip()
keyword2_positive_percent = input_content[8].split(',')[2].strip()

keyword3_name = input_content[9].split(',')[0].strip()
keyword3_count = input_content[9].split(',')[1].strip()
keyword3_positive_percent = input_content[9].split(',')[2].strip()

keyword4_name = input_content[10].split(',')[0].strip()
keyword4_count = input_content[10].split(',')[1].strip()
keyword4_positive_percent = input_content[10].split(',')[2].strip()


category_name = input_content[11].split(',')[0].strip()
category_count = input_content[11].split(',')[1].strip()
category_positive_percent = int(input_content[11].split(',')[2].strip())

category_tag = 'Great !!! 🎉'

if category_positive_percent < 60 and category_positive_percent >= 30 :
    category_tag = 'Good !!! 💪'

if category_positive_percent < 30 and category_positive_percent >= 0 :
    category_tag = 'Not Bad !!! 😐'

        

print(colored(youtube_channel_name, 'red'))
print(colored(youtube_video_title, 'red'))
print(colored(youtube_video_url, 'red'))


email_template = f""" 
Dear {youtube_channel_name} Youtube Channel Admin,

I hope you're doing well. My name is Taha, an AI software developer. I am reaching out to you to share the results of my recent analysis of your YouTube video using commentsanalytics.com - an AI tool that provides comprehensive insights into YouTube comments 💬.

After analyzing your recent video "{youtube_video_title}" ({youtube_video_url}) using CommentsAnalytics, I have gathered some valuable findings 🔍 that I would like to share with you. 💡

Here is a summary of the analysis:

Sentiment Analysis: The sentiment breakdown of the comments is as follows:

Positive 🤩: {positive_percent}%
Neutral 😐: {neutral_percent}%
Negative 🥴: {negative_percent}%
It's encouraging to see that the majority of comments are {dominant_sentiment}. ({dominant_tag})
Keyword Extraction: The most frequent keywords mentioned in the comments include "
{keyword1_name}({keyword1_count} - {keyword1_positive_percent}% Positive),
{keyword2_name}({keyword2_count} - {keyword2_positive_percent}% Positive),
{keyword3_name}({keyword3_count} - {keyword3_positive_percent}% Positive),
{keyword4_name}({keyword4_count} - {keyword4_positive_percent}% Positive)
 and more. These keywords provide insights into the topics that resonated with your audience.

Comment Categories: The most dominant comment category was "{category_name}" with {category_count} comments. These comments had an overall positive sentiment of {category_positive_percent}% ({category_tag}). These categories can prioritize and address comments efficiently for reply and improved customer satisfaction 🎯 🚀.

I have attached detailed charts and Excel sheets with the complete analysis for your reference . 💥📊

CommentsAnalytics offers a comprehensive solution for understanding audience sentiment through advanced keyword extraction and named-entity recognition. By categorizing comments based on their purposes, such as questions or feedback, you can respond more efficiently and effectively. The tool is user-friendly, providing accurate results and allowing you to focus on creating engaging content while we handle the analysis.

I invite you to visit commentsanalytics.com and sign up for CommentsAnalytics to experience the power of our tool yourself 🤝. As a gesture of appreciation for your partnership, I have provided a 100% discount code "FEEDBACK100" for the starter plan. You can simply export each video using the Chrome extension available on our website.

As a newcomer in the field of comment analysis, I value your feedback on the analysis and any suggestions you may have for further improvements 🙏. Your insights will be instrumental in refining our services.

Thank you for your time and consideration.

Best regards,
Taha
"""

output_email_file.write(email_template)
output_email_file.close()
