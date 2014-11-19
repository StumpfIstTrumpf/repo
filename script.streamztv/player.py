# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 13:29:35 2014

@author: stumpf
"""

import xbmc, xbmcgui, xbmcaddon, getter, gui, time



class MyPlayer(xbmc.Player):
    
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)

    def setcallback(self, Startcallback):
        self.startcall = Startcallback
        
    def setplaylist(self,listing):
        self.playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        self.playlist.clear()
        for item in listing:
            listItem = xbmcgui.ListItem(label=item['title'],iconImage=item['image'],thumbnailImage=item['image'])
            self.playlist.add(item['url'],listItem)    
    def setGUI(self, GUI):
        self.gui = GUI
    def playStream(self):
        #self.playlist.shuffle()
        self.play(self.playlist)
        self.gui.show()
        #self.playselected(3)
        
    def Count(self):
        return len(xbmc.PlayList(xbmc.PLAYLIST_VIDEO))

    def Index(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition()

    def onPlayBackStarted(self):
        self.startcall()
        self.gui.show()

    def onPlayBackPaused(self):
        pass     

    def onPlayBackResumed(self):
        self.gui.show()   

    def onPlayBackEnded(self):
        pass

    def onPlayBackStopped(self):        
        pass

    def onPlayBackSeek(self, time, seekOffset):
        pass       

    def onPlayBackSeekChapter(self, chapter):
        pass       

    def onPlayBackSpeedChanged(self, speed):
        pass       

    def onQueueNextItem(self):
        self.gui.show()
