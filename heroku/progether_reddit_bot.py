#! /usr/bin/python

import requests
import json
import socket

def shorten(url):
    bitly_username = "projectdelphai"
    bitly_api_key = "R_8e6bd9705f556e6c428bf0fc1835fb2e"
    api_url = "https://api-ssl.bitly.com/v3/shorten?access_token=3009c360766239e95a5d3e6ac04ac01539860bb4&longUrl=%s" % url
    r = requests.get(api_url)
    data = json.loads(r.text)
    shortened_url = data['data']['url']
    return shortened_url

def get_latest_post():
    url = "http://www.reddit.com/r/progether/new.json"
    r = requests.get(url)
    data = json.loads(r.text)
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
    
post_to_irc(get_latest_post())
