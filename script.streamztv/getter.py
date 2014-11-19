# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 13:29:35 2014

@author: stumpf
"""

import sys, os, xbmcgui, xbmc, xbmcplugin, xbmcaddon, time

sys.path.append(xbmc.translatePath( os.path.join( xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'lib' ) ))

import requests, simplejson, re

__settings__   = xbmcaddon.Addon(xbmcaddon.Addon().getAddonInfo('id'))

def getUserdata():
    global thisPlugin
    username = __settings__.getSetting("username")
    password = __settings__.getSetting("password")
    return username, password


def trylogin():
    user, passw = getUserdata()
    r = requests.get('http://stream4k.net/xbmc-logins.php?username='+ user +'&password='+ passw)
    response = simplejson.loads(r.text)
    
    if (response["success"]=="true"):
        return response["securetoke"]
    else:
        return False
 
def getplaylist():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0','Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    user = getUserdata()[0]
    passw = getUserdata()[1]
    resp    = requests.get('http://stream4k.net/stream-channel.php?u='+ user +'&p='+ passw,headers=headers)

    response = resp.text

    playlist = simplejson.loads(response)
    plitem = {}
    pllist = []
    for i in range(0,len(playlist)):
        if ((i%4)== 0):
            plitem.update({"title":playlist[i]})
        elif ( i % 4 ==1):
            plitem.update({"description":playlist[i]})
        elif (i%4==2):
            plitem.update({"file":playlist[i]})
        elif (i%4==3):
            plitem.update({"image":playlist[i]})
            pllist.append(plitem.copy())

    return pllist


def getepg(sender):
    sender = sender.replace(" ", "");
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection': 'keep-alive','Accept-Encoding': 'gzip, deflate','Accept-Language': 'de,en-US;q=0.7,en;q=0.3'}
    session = requests.Session()
    link    = 'http://eydu.hol.es/?sender='+sender.replace("+","%2B")
    #link    = 'http://forum.stream4k.net/epg/default.php?sender='+sender.replace("+","%2B")
    resp    = session.get(link,headers=headers)
    response = resp.text
    print link
    if(response==""):
        return "null"
    else:    
        #print response
        try:
            return simplejson.loads(response)
        except:
            return getepg(sender)