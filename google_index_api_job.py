#@title **Provide Complete Path Of The API Key Here**
API_Path = "social-browse-339619-a2d0553b073b.json"

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import datetime

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
print('*'*50);print("Scopes & Endpoint Configured...");print('*'*50);print("Adding Key...");print('*'*50);
# service_account_file.json is the private key that you created for your service account.
JSON_KEY_FILE = API_Path
print("Key Added Successfully!");print('*'*50);
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())
print("Credentials Successfully Authorized!");print('*'*50);

####################################################################################################################

#@title **Provide Site URL & Update Request Type**
#@markdown Site URL will the exact URL you want to update or delete from the Google Search Index. **Also, please make a note that you have to provide URL only for the ownership verfied website. For any other URLs, it will not work.**
siteURL = "https://profilebrowse.com/services_twitter/" #@param {type:"string"}
requestType = "URL_UPDATED" #@param ["URL_UPDATED", "URL_DELETED"]
content = str({'url':siteURL,'type':requestType})
print("RESULT:");print('*'*50);print("URL and Update Request Type Configured!");print('*'*50);

while True:
    response, content = http.request(ENDPOINT, method="POST", body=content)
    output = response['status']

    if output == '200':
        print("Successfully Done!");print('*'*50);
        break

    else:
        print("Error Code: {}".format(output) + "  >>>>  " +  str(datetime.datetime.now()));print('*'*50);
        # print("Visit Here For More: https://developers.google.com/search/apis/indexing-api/v3/core-errors#api-errors");
        # print('*'*50);