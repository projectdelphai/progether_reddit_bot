#!/usr/bin/env python

import webapp2
import json
from google.appengine.api import urlfetch
from local_settings import bitly_username,bitly_api_key

import json
import socket

def shorten(url):
    api_url = "https://api-ssl.bitly.com/v3/shorten?access_token=3009c360766239e95a5d3e6ac04ac01539860bb4&longUrl=%s" % url
    #r = requests.get(api_url)
    #using urlfetch instead of requests because that doesnt work on appengine
    r = urlfetch.fetch(url=api_url,
        method=urlfetch.GET,
        headers={'Content-Type': 'application/json'})
    content = json.loads(r.content)
    data = json.loads(r.content)
    shortened_url = data['data']['url']
    return shortened_url

def get_latest_post():
    url = "http://www.reddit.com/r/progether/new.json"
    #r = requests.get(url)
    #data = json.loads(r.text)
    data = json.loads(urlfetch.fetch(url).content)
    latest = data['data']['children'][0]['data']
    title = latest['title']
    short_url = shorten(latest['url'])
    author = latest['author']
    latest_post = "\"%s\" by %s (%s)" % (title,author,short_url)
    return latest_post

def post_to_irc(post_string):
    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_socket.connect(("irc.freenode.net", 6667))
    string = 'NICK %s \r\n' % "reddit_progether_bot"
    irc_socket.send(string.encode("UTF-8"))
    string = 'USER %s some stuff :Python IRC\r\n' % "reddit_progether_bot"
    irc_socket.send(string.encode("UTF-8"))
    string = 'JOIN %s \r\n' % "#reddit-progether"
    irc_socket.send(string.encode("UTF-8"))
    while (True):
        received_data = irc_socket.recv(4096).decode("UTF-8")
        print(received_data.encode("UTF-8"))
        if received_data.find('PING') != -1:
            print(received_data)
            string = 'PONG %s \r\n' % received_data.split()[1]
            irc_socket.send(string.encode("UTF-8"))
        if received_data.find('JOIN #reddit-progether') != -1:
            string = 'PRIVMSG #reddit-progether :%s\r\n' % post_string
            irc_socket.send(string.encode("UTF-8"))
            break

class Bot(webapp2.RequestHandler):
    def get(self):
        post_to_irc(get_latest_post())
        self.response.write( get_latest_post() )

application = webapp2.WSGIApplication([
    ('/', Bot)
    ],debug=True)