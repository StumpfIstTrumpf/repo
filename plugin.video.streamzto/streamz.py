# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 00:18:50 2014

@author: stumpf
"""
import sys, os, xbmcgui, xbmc, xbmcplugin, xbmcaddon
from math import *

sys.path.append(xbmc.translatePath( os.path.join( xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'lib' ) ))

import requests, simplejson, re

thisPlugin = int(sys.argv[1])

##############################################################

def getUserdata():
    global thisPlugin
    username = xbmcplugin.getSetting(thisPlugin,"username")
    password = xbmcplugin.getSetting(thisPlugin,"password")
    return username, password
    
def getplaylist(user,passw):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0','Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    user = getUserdata()[0]
    passw = getUserdata()[1]
    resp    = requests.get('http://stream4k.net/stream-channel.php?u='+ user +'&p='+ passw,headers=headers)
    response = resp.text

    playlist = simplejson.loads(response)
    plitem = {}
    pllist = []
    print playlist
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
    print pllist

    return pllist


    
##############################################################  


def createListing(token,user,passw):
    listing = []
    infos = getplaylist(user,passw)
    for info in infos:
        listing.append([info['title']+" | "+info['description'], info['file']+" swfurl=http://forum.stream4k.net/ips_kernel/test/playering/jwplayerxbmc/jwplayer.flash.swf live=true token="+token, info['image']])
 
    return listing


def sendToXbmc(listing):
    global thisPlugin
    for item in listing:
        listItem = xbmcgui.ListItem(label=item[0],iconImage=item[2],thumbnailImage=item[2])
        xbmcplugin.addDirectoryItem(thisPlugin,item[1],listItem)
    xbmcplugin.endOfDirectory(thisPlugin)


def main():
    user = getUserdata()[0]
    passw = getUserdata()[1]
    r = requests.get('http://stream4k.net/xbmc-logins.php?username='+ user +'&password='+ passw)

    response = simplejson.loads(r.text)
    if (response["success"]=="true"):
        sendToXbmc(createListing(response["securetoke"],user,passw))
        
    else:
        title = "Login Fehlgeschlagen"
        text = "Login falsch oder Dein Premium ist abgelaufen"
        time = 5000  # ms
        xbmc.executebuiltin('Notification(%s, %s, %d)'%(title, text, time))
    
    
main()






