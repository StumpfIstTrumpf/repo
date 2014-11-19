# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 13:29:35 2014

@author: stumpf
"""

import xbmc, xbmcaddon, time, gui, player, getter
from thread import start_new_thread

thegui = gui.Window("test.xml", xbmcaddon.Addon().getAddonInfo('path'))
__icon__        = xbmcaddon.Addon().getAddonInfo('icon')

playlist = []
virgin = True

def makeplaylist():
    return getter.getplaylist()

def playerstarted():
    global thegui
    global virgin
    time.sleep(1)
    thegui.myshow()
    time.sleep(2)
    thegui.myshow()
    
    
def setEPG():
    global thegui
    start_new_thread(thegui.loadepglist,())
    

def correctnames(name):
    if "sky sport news" in name.lower():
        return "Sky Sport News HD"
    elif "sky cinema" in name.lower():
        return "Sky Cinema"
    elif "sky action" in name.lower():
        return "Sky Action"
    elif "discovery" in name.lower():
        return "Discovery Channel"
    elif "national" in name.lower():
        return "National Geographic"
    elif "history" in name.lower():
        return "History HD"
    elif "spiegel" in name.lower():
        return "Spiegel Geschichte HD" 
    elif "atlantic" in name.lower():
        return "Sky Atlantic HD" 
    elif "sport1 us" in name.lower():
        return "Sport1 US HD"
    elif "sport1+" in name.lower(): 
        return "Sport1+ HD"
    elif "sky bundesliga" in name.lower():
        if "1" in name.lower():
            return "Sky Bundesliga HD1"
        elif "2" in name.lower():
            return "Sky Bundesliga HD2"
        elif "3" in name.lower():
            return "Sky Bundesliga HD3"
        elif "4" in name.lower():
            return "Sky Bundesliga HD4"
        elif "5" in name.lower():
            return "Sky Bundesliga HD5"
        elif "6" in name.lower():
            return "Sky Bundesliga HD6"
        elif "7" in name.lower():
            return "Sky Bundesliga HD7"
        elif "8" in name.lower():
            return "Sky Bundesliga HD8"
        elif "9" in name.lower():
            return "Sky Bundesliga HD9"
        elif "10" in name.lower():
            return "Sky Bundesliga HD10"
    elif "sport" in name.lower():
        if "1" in name.lower():
            return "Sky Sport HD1"
        elif "2" in name.lower():
            return "Sky Sport HD2"
        elif "3" in name.lower():
            return "Sky Sport HD3"
        elif "4" in name.lower():
            return "Sky Sport HD4"
        elif "5" in name.lower():
            return "Sky Sport HD5"
        elif "6" in name.lower():
            return "Sky Sport HD6"
        elif "7" in name.lower():
            return "Sky Sport HD7"
        elif "8" in name.lower():
            return "Sky Sport HD8"
        elif "9" in name.lower():
            return "Sky Sport HD9"
        elif "10" in name.lower():
            return "Sky Sport HD10"
    else:
        return name

def reloadplaylist():
    login = getter.trylogin()
    if (login!=False):
        playlist = makeplaylist()
        for item in playlist:
            item["url"] = item['file'] +" swfurl=http://forum.stream4k.net/ips_kernel/test/playering/jwplayerxbmc/jwplayer.flash.swf live=true token="+login
            item["title"] = correctnames(item["title"])
        channel.setplaylist(playlist)
        thegui.setplaylist(playlist) 
        channel.playStream()   
        thegui.loadepglist()

if __name__ == '__main__':
    title = "Startet"
    text = "Kann einen Moment lang dauern"
    timems = 4000  # ms
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, text, timems, __icon__))
    login = getter.trylogin()
    if (login!=False):
        playlist = makeplaylist()
        for item in playlist:
            item["url"] = item['file'] +" swfurl=http://forum.stream4k.net/ips_kernel/test/playering/jwplayerxbmc/jwplayer.flash.swf live=true token="+login
            item["title"] = correctnames(item["title"])
            
        #iniPlayer
        channel = player.MyPlayer()
        channel.setcallback(playerstarted)
        channel.setplaylist(playlist)


        #ini gui
        thegui.setcallback(setEPG)
        thegui.setreloadplaylist(reloadplaylist)
        thegui.setplayer(channel)
        thegui.setplaylist(playlist)        
  
        channel.setGUI(thegui)          
        channel.playStream()      
         
        thegui.doModal()

        #beenden
        del thegui
        channel.stop()
        del channel
        xbmc.executebuiltin( "XBMC.ActivateWindow(10006)" )
        
    else:
        title = "Login Fehlgeschlagen"
        text = "Login falsch oder Dein Premium ist abgelaufen"
        timems = 5000  # ms
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, text, timems, __icon__))

