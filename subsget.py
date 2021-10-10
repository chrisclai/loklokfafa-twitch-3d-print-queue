from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

##########################################################
#                Configure your stuff here               #
##########################################################

import privinfo

clientId= privinfo.extension_id #Register a Twitch Developer application and put its client ID here
accessToken= privinfo.extension_oauth #Generate an OAuth token with channel_subscriptions scope and insert your token here
 
channelName= "loklokfafa"  #Put your channel name here
saveLocation = "/privstuff/subscriberList.txt" #Put the location you'd like to save your list here
 
###################################################################
 
session = Session()
channelId = privinfo.channel_id
result = None
response = None
 
apiRequestUrl = "https://api.twitch.tv/helix/subscriptions?broadcaster_id=" + channelId
 
# Do the API Lookup
headers = {'Client-ID': clientId, 'Accept': 'application/vnd.twitchtv.v5+json', 'Authorization': 'Bearer '+accessToken, 'Content-Type': 'application/json'}
response = session.get(apiRequestUrl, headers=headers)
try:
    result = json.loads(response.text)
except:
    result = None

# Filter out API sourced dictionary to return only subs from channel (Sub Scraper)
print("List of Subscribers:")
if result:
    subList=[]
    for x in result['data']:
        subname = x['user_name']
        
        if subname != channelName:
            subList.append(subname)
            print(subname)