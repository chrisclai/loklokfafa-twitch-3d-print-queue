from hashlib import new
from logging import exception
import discord
import irc.bot
import requests
import random
import time
from datetime import datetime

from requests.models import StreamConsumedError
import privinfo
from _thread import *
import threading
# import tkinter as tk
from pygame import mixer

# Individual File Dependencies
from updatejson import *
from subsget import *

class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print ('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        print ('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        
        # Put your channel name here
        channelName = "loklokfafa"
        
        if e.arguments[0][:13] == '!printrequest':
            subs = getSubsList()
            if e.source.nick in subs:
                try:
                    name, link = e.arguments[0].split(' ')[1], e.arguments[0].split(' ')[2]
                    print(f'New Print Request Queued from user {e.source.nick}: {link}')
                    self.add_print(e, name, link)
                except Exception as f:
                    print(f"Queue Command Failed. Reason: {f}")
                    c.privmsg(self.channel, f"Hello {e.source.nick}, what would you like to 3D print today? (Format: !printrequest <printname> <printlink>")
            else:
                c.privmsg(self.channel, f"Sorry, this command is limited to subscribers only!")
        if e.arguments[0][:16] == '!completerequest':
            if e.source.nick == channelName.lower():
                print(f"Removing current print from top of the queue!")
                self.remove_print(e)
            else:
                c.privmsg(self.channel, "Sorry, this command can only be used by the broadcaster.")
        elif e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)

    def remove_print(self, e):
        c = self.connection
        filelocation = 'privstuff/printqueue.json' # Change based on individual version
        requests = refresh_json(filelocation)
        
        try:
            username = requests['1']['username']
            requests = remove_element(requests)
            print(len(requests))
            if len(requests) == 1:
                requests['0']['username'] = 'PLACEHOLDER'
                requests['0']['printlink'] = 'PLACEHOLDER'
                requests['0']['printname'] = 'PLACEHOLDER'
                requests['0']['daterequest'] = 'PLACEHOLDER'
            update_json(requests, filelocation)
            c.privmsg(self.channel, f"Completed {username}'s request! Thank you for using QueueBot!")
        except:
            c.privmsg(self.channel, "There are currently no requests!")

    def add_print(self, e, name, link):
        c = self.connection
        filelocation = 'privstuff/printqueue.json' # Change based on individual version
        requests = refresh_json(filelocation)
        now = datetime.now()

        # Add new element into dictionary
        requests[str(len(requests))] = new_element(['username', 'printlink', 'printname', 'daterequest'])
        
        # Refresh dictionary
        update_json(requests, filelocation)
        requests = refresh_json(filelocation)

        # Fill out dictionary elements
        requests[str(len(requests) - 1)]['username'] = e.source.nick
        requests[str(len(requests) - 1)]['printlink'] = link
        requests[str(len(requests) - 1)]['printname'] = name
        requests[str(len(requests) - 1)]['daterequest'] = now.strftime('%m/%d/%Y')

        # Place data into json file
        update_json(requests, filelocation)
        c.privmsg(self.channel, f"Hello {e.source.nick}, your request has been successfully activated in the queue! Thank you for participating!")
                    
    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            print(self.channel_id)
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently streaming: ' + r['status'])

        # Poll the API to let the user know if they are a subscriber of the channel
        elif cmd == "amiasub":
            subs = getSubsList()
            if e.source.nick in subs:
                message = f"{e.source.nick}, Yes, you are a sub to the channel."
            else:
                message = f"{e.source.nick}, No, you are not a sub to the channel."
            c.privmsg(self.channel, message)

def main():
    username  = "crackncheesebot"
    client_id = privinfo.client_id
    token     = privinfo.token
    channel   = "loklokfafa"

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()