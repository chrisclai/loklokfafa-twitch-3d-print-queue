from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

def getSubsList():
    import privinfo

    clientId = privinfo.extension_id #Register a Twitch Developer application and put its client ID here
    accessToken = privinfo.extension_oauth #Generate an OAuth token with channel_subscriptions scope and insert your token here
    
    channelName = "loklokfafa"  #Put your channel name here
    
    # Channel Info
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
    subList = []
    if result:
        for x in result['data']:
            subname = x['user_name']
            subList.append(subname.lower())

    # Return a list containing all subs in the channel
    return subList