# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 13:29:35 2014

@author: stumpf
"""
import xbmc, xbmcgui, gui, xbmcaddon, time, getter, player, string
from threading import Timer
from thread import start_new_thread
from math import *

ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_NAV_BACK = 92
ACTION_SELECT_ITEM = 7
ACTION_MOVE_RIGHT = 1
ACTION_MOVE_LEFT = 2
ACTION_KONTEXT = 24

ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_RIGHT_CLICK = 101

KEY_BUTTON_BACK = 275
KEY_KEYBOARD_ESC = 61467

KEY_G = 61511
KEY_O = 61519
KEY_L = 61516
KEY_U = 61525

SKIN_PLAYER = 4100
SKIN_EPG_VISIBILITY_MARKER = 5000
SKIN_TVINFO_VISIBILITY_MARKER = 5001
SKIN_TVINFO_CHANNEL = 4102
SKIN_TVINFO_CHTHUMB = 4103
SKIN_TVINFO_TITEL = 4104
SKIN_TVINFO_UNTERTITEL = 4105
SKIN_TVINFO_LAENGE = 4106
SKIN_TVINFO_ZEIT = 4107
SKIN_TVINFO_BESCHREIBUNG = 4108
SKIN_TVINFO_DARSTELLER = 4109
SKIN_TVINFO_INFOS = 4110

SKIN_EPG_HEAD_DATE = 4001
SKIN_EPG_HEAD_1HALF = 4002
SKIN_EPG_HEAD_2HALF = 4003
SKIN_EPG_HEAD_3HALF = 4004
SKIN_EPG_HEAD_4HALF = 4005
SKIN_EPG_HEAD_5HALF = 4006
SKIN_EPG_TVINFO_TITEL = 4010
SKIN_EPG_TVINFO_UNTERTITEL = 4011
SKIN_EPG_TVINFO_LAENGE = 4012
SKIN_EPG_TVINFO_BESCHREIBUNG = 4013
SKIN_EPG_TVINFO_INFOS = 4014

SKIN_PATH_BUTTON_FOCUS = "epg/buttonfocus.png"
SKIN_PATH_BUTTON_NOFOCUS = "epg/buttonnofocus.png"
SKIN_EPG_LINE = 4090

MAX_SENDER = 7

class Window(xbmcgui.WindowXML):
    def __init__(self,strXMLname, strFallbackPath):
        """
            Changing the three varibles passed won't change, anything
            Doing strXMLname = "bah.xml" will not change anything.
            don't put GUI sensitive stuff here (as the xml hasn't been read yet
            Idea to initialize your variables here
        """
        self.epglist = []
        self.playlist = []
        self.virgin = True
        self.info = False
        self.epgloaded = False
        self.uhran = True
        self.modus = "Full"
        #EPG
        self.buttons = []
        self.imgs = []
        self.buttoninfos ={}
        self.navpos = 0

    def onInit(self):
        """
            This function has been implemented and works
            The Idea for this function is to be used to get initial data and populate lists
        """
        #self.getControl(SKIN_EPG_VISIBILITY_MARKER).setVisible(True)

        if(self.virgin):
            self.epgviewup = xbmcgui.ControlButton(-1, -1, 1, 1, "")
            self.addControl(self.epgviewup)
            self.epgviewup.setVisibleCondition('[!Control.IsVisible('+str(SKIN_EPG_VISIBILITY_MARKER)+')]') 
            print self.epgviewup.getId()
            self.epgviewdown = xbmcgui.ControlButton(-1, -1, 1, 1, "")
            self.addControl(self.epgviewdown)
            self.epgviewdown.setVisibleCondition('[!Control.IsVisible('+str(SKIN_EPG_VISIBILITY_MARKER)+')]') 
            print self.epgviewdown.getId()

            self.virgincall()
            self.virgin = False
            self.hideinfo()

        lt = time.localtime()
        aktH, aktM = lt[3:5]
        aktH -= 6
        if(aktH < 0):
            aktH += 24
        #start_new_thread(self.uhr,())
    
    def redraw(self):
        """
            This redraws
        """
        if(self.modus=="Full"):
            self.getControl(SKIN_EPG_VISIBILITY_MARKER).setVisible(True)
        elif(self.modus=="EPG"):
            self.getControl(SKIN_EPG_VISIBILITY_MARKER).setVisible(False)
            time.sleep(0.7)
            self.setFocus(self.butnav[0][0])

            
    def setcallback(self, virgincallback):
        self.virgincall = virgincallback
        
    def hideinfo(self):
        self.getControl(SKIN_TVINFO_VISIBILITY_MARKER).setVisible(False)
        
    def showinfo(self):
        if(self.epgloaded):
            self.drawinfo()
        self.uhr()
        self.getControl(SKIN_TVINFO_VISIBILITY_MARKER).setVisible(True)

    def drawinfo(self):
        index = self.player.Index()
        aktidx = self.findcurrent(index)
        self.getControl(SKIN_TVINFO_CHANNEL).setLabel(self.playlist[index]["title"])
        
        self.getControl(SKIN_TVINFO_CHTHUMB).setImage(self.getlogopath(self.playlist[index]["title"],"logos"))
        startH, startM = self.epglist[index][aktidx]["zeit"].split(":")
        startH = int(startH)
        startM = int(startM)
        laenge = self.epglist[index][aktidx]["laenge"].replace(" min.","")
        if(laenge != ''):
            laenge = int(laenge)
        else:
            laenge = 60
            
        endeM = startM + laenge
        n = (endeM / 60)
        endeH = startH + n
        endeM -= n*60
        dauer = str(startH).zfill(2)+":"+str(startM).zfill(2)+" - "+str(endeH).zfill(2)+":"+str(endeM).zfill(2)
        self.getControl(SKIN_TVINFO_LAENGE).setLabel(dauer)
        
        infos = "Informationen:\n"
        infos = (infos + self.epglist[index][aktidx]["genrejahr"] + "\n") if self.epglist[index][aktidx]["genrejahr"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["laenge"] + "") if self.epglist[index][aktidx]["laenge"] != "" else (infos + "")
        infos = (infos + ", " + self.epglist[index][aktidx]["FSK"] + "\n") if self.epglist[index][aktidx]["FSK"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["regie"] + "\n") if self.epglist[index][aktidx]["regie"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["drehbuch"] + "\n") if self.epglist[index][aktidx]["drehbuch"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["kamera"] + "\n") if self.epglist[index][aktidx]["kamera"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["musik"] + "\n") if self.epglist[index][aktidx]["musik"] != "" else (infos + "")
        
        self.getControl(SKIN_TVINFO_INFOS).setLabel(infos)
        self.getControl(SKIN_TVINFO_TITEL).setLabel(self.epglist[index][aktidx]["titel"])
        self.getControl(SKIN_TVINFO_UNTERTITEL).setLabel(self.epglist[index][aktidx]["episodentitel"].replace("Episodentitel: ",""))

        self.getControl(SKIN_TVINFO_BESCHREIBUNG).setLabel(self.epglist[index][aktidx]["beschreibung"])
        self.getControl(SKIN_TVINFO_DARSTELLER).setLabel(self.epglist[index][aktidx]["darsteller"].replace(": ",":\n").replace(", ","\n"))

    def loadepglist(self):
        for item in self.playlist:
            self.epglist.append(getter.getepg(item["title"]))
        self.epgloaded = True
        self.myshow()
        self.onGuideButton()
    
    def findcurrent(self,senderid):
        lt = time.localtime()
        aktH, aktM = lt[3:5]
        aktH -= 6
        if(aktH < 0):
            aktH += 24
        iterator = 0
        go = True
        while(go):
            sendung = self.epglist[senderid][iterator] if iterator < len(self.epglist[senderid]) else -1
            if(sendung == -1):
                iterator -= 1
                return iterator
            startH, startM = sendung["zeit"].split(":")
            startH = int(startH)
            startM = int(startM)
            startH -= 6
            if(startH < 0):
                startH += 24
            if((startH>aktH)or(startH>=aktH and startM>aktM)):
                go = False
                iterator -= 1
            else:
                iterator += 1
        return iterator
              
    def setreloadplaylist(self,func):
        self.reloadplaylist = func

    def setplaylist(self, listing):
        self.playlist = listing
        
    def setplayer(self, player):
        self.player = player

    def uhr(self):
        lt = time.localtime()
        aktH, aktM = lt[3:5]
        aktH = str(aktH).zfill(2)
        aktM = str(aktM).zfill(2)
        self.getControl(SKIN_TVINFO_ZEIT).setLabel(aktH+":"+aktM)
#        if(self.uhran):
#            self.uhr()
        
    def getlogopath(self,name,what):
        if "sky sport news" in name.lower():
            return what+"/news.png"
        elif "sky cinema" in name.lower():
            return what+"/cinema.png"
        elif "sky action" in name.lower():
            return what+"/action.png"
        elif "discovery" in name.lower():
            return what+"/discover.png"
        elif "national" in name.lower():
            return what+"/national.png"
        elif "spiegel" in name.lower():
            return what+"/geschichte.png"
        elif "atlantic" in name.lower():
            return what+"/atlantic.png"
        elif "history" in name.lower():
            return what+"/history.png"
        elif "sport1 us" in name.lower():
            return what+"/sportus.png"
        elif "sport1+" in name.lower(): 
            return what+"/sporteins.png"
        elif "sky bundesliga" in name.lower():
            if "1" in name.lower():
                return what+"/buli1.png"
            elif "2" in name.lower():
                return what+"/buli2.png"
            elif "3" in name.lower():
                return what+"/buli.png"
            elif "4" in name.lower():
                return what+"/buli.png"
            elif "5" in name.lower():
                return what+"/buli.png"
            elif "6" in name.lower():
                return what+"/buli.png"
            elif "7" in name.lower():
                return what+"/buli.png"
        elif "sport" in name.lower():
            if "1" in name.lower():
                return what+"/sport1.png"
            elif "2" in name.lower():
                return what+"/sport2.png"
            elif "3" in name.lower():
                return what+"/sport3.png"
            elif "4" in name.lower():
                return what+"/sport.png"
            elif "5" in name.lower():
                return what+"/sport.png"
            elif "6" in name.lower():
                return what+"/sport.png"
        else:
            return what+"/dummy.png"

    def myshow(self):
        if(self.epgloaded):
            self.drawinfo()
        self.uhr()
        self.show()

    def getdatestr(self,time):
        monat, tag = time[1:3]
        wochentag = time[6]
        if wochentag == 0:
            wochentag = "Montag"
        elif wochentag == 1:
            wochentag = "Dienstag"
        elif wochentag == 2:
            wochentag = "Mittwoch"
        elif wochentag == 3:
            wochentag = "Donnerstag"
        elif wochentag == 4:
            wochentag = "Freitag"
        elif wochentag == 5:
            wochentag = "Samstag"
        elif wochentag == 6:
            wochentag = "Sonntag"
        return wochentag+", "+str(tag)+"."+str(monat)+"."

    def onGuideButton(self):
        lt = time.localtime()      
        aktH, aktM = lt[3:5]
        aktM -= 10
        if (aktM<0):
            aktH -= 1
            aktM += 60
        self.drawhead(aktH, aktM)
        self.navtoppos = 0
        self.drawEPG(aktH, aktM, self.epglist[0:MAX_SENDER])

    def drawallepg(self,todolist):
        lt = time.localtime()      
        aktH, aktM = lt[3:5]
        aktM -= 10
        if (aktM<0):
            aktH -= 1
            aktM += 60
        self.drawhead(aktH, aktM)
        print "Start"
        self.drawEPG(aktH, aktM, todolist)

    def drawhead(self,startH, startM):
        lt = time.localtime()
        self.getControl(SKIN_EPG_HEAD_DATE).setLabel(self.getdatestr(lt))
        halfM = startM
        halfH = startH
        for i in range(0,5):
            if (halfM <= 30): 
                halfM = 30 
            else:
                halfM = 0
                halfH += 1
                halfH = halfH % 24
            start = 165 + 440 * ((halfH+(halfM/60.0))-(startH+(startM/60.0))) - 65 #offset
            self.getControl(SKIN_EPG_HEAD_1HALF+i).setPosition(int(start), 5)
            self.getControl(SKIN_EPG_HEAD_1HALF+i).setLabel(str(halfH).zfill(2)+":"+str(halfM).zfill(2))
            halfM = (halfM + 30)
    

    # def redrawEPGdown(self):
    #     #newbie = True
    #     if(self.navpos < len(self.playlist)-MAX_SENDER):
    #         for img in self.imgs:
    #             img.setPosition(img.getPosition()[0],img.getPosition()[1]-64)
            
    #         for channel in self.butnav:
    #             for item in channel:
    #                 item.setPosition(item.getPosition()[0],item.getPosition()[1]-64)

    #         self.removeControl(self.imgs[0])
    #         self.imgs.remove(self.imgs[0])

    #         for fitem in self.butnav[0]:
    #             self.removeControl(fitem)
    #             self.buttons.remove(fitem)
            
    #         self.butnav.remove(self.butnav[0])

    #         #Draw new one




    def drawEPG(self,rangeaH,rangeaM,todolist):
        rangeaH -= 6
        if(rangeaH < 0):
            rangeaH += 24
        rangeeH = rangeaH + 2
        rangeeM = (rangeaM + 30) % 60
        
        
        for item in self.buttons:
            try:
                self.removeControl(item)
            except:
                pass
        
        for item in self.imgs:
            try:
                self.removeControl(item)
            except:
                pass
            
        self.buttons = []
        self.imgs = []
        self.buttoninfos ={}
        self.butnav = []
        
        if (self.epgloaded):
            lt = time.localtime()
            aktH, aktM = lt[3:5]
            aktH -= 6
            if(aktH < 0):
                aktH += 24
            if(aktH > rangeaH or (aktH==rangeaH and aktM>rangeaM)) and (aktH<rangeeH or (aktH==rangeeH and aktM<rangeeM)):
                start = 165 + 440 * ((aktH+(aktM/60.0))-(rangeaH+(rangeaM/60.0)))
                self.getControl(SKIN_EPG_LINE).setPosition(int(start), 5)

                
            y = -3
            c = 0
            
            for channel in todolist:
                self.butnav.append([])
                c += 1
                y += 64 
                if (channel=="null"):
                    continue
                cannelidx = todolist.index(channel)
                playlistidx = self.epglist.index(channel)
                tempimg = xbmcgui.ControlImage(15, y-1, 146, 64, filename = self.getlogopath(self.playlist[todolist.index(channel)]["title"],"epg"))
                self.addControl(tempimg)
                tempimg.setVisibleCondition('[!Control.IsVisible('+str(SKIN_EPG_VISIBILITY_MARKER)+')]') 
                tempimg.setImage(self.getlogopath(self.playlist[self.epglist.index(channel)]["title"],"epg"))
                self.imgs.append(tempimg)
                
                iterator = 0
                for sendung in channel:
                    iterator +=1
                    drawble = False
                    
                    startH, startM = sendung["zeit"].split(":")
                    startH = int(startH)
                    startM = int(startM)
                    startH -= 6
                    if(startH < 0):
                        startH += 24
                        
                    laenge = sendung["laenge"].replace(" min.","")
                    
                    if(laenge != ''):
                        laenge = int(laenge)
                    else:
                        laenge = 60
                        
                    endeM = startM + laenge
                    n = (endeM / 60)
                    endeH = startH + n
                    endeM -= n*60
                    if(startH < rangeaH or (startH==rangeaH and startM<rangeaM)) and (endeH>rangeeH or (endeH==rangeeH and endeM>rangeeM)):#allout
                        start = 166
                        width = 1100
                        drawble = True
                    elif(startH > rangeaH or (startH==rangeaH and startM>rangeaM)) and (endeH<rangeeH or (endeH==rangeeH and endeM<rangeeM)):#allin
                        start = 165 + 440 * ((startH+(startM/60.0))-(rangeaH+(rangeaM/60.0)))
                        width = laenge*(1100.0/150.0)
                        width = int(width)
                        drawble = True
                    elif(startH > rangeaH or (startH==rangeaH and startM>rangeaM)) and (startH<rangeeH or (startH==rangeeH and startM<rangeeM)):#ende out
                        start = 165 + 440 * ((startH+(startM/60.0))-(rangeaH+(rangeaM/60.0)))
                        width = 1265 - start
                        drawble = True
                    elif(endeH > rangeaH or (endeH==rangeaH and endeM>rangeaM)) and (endeH<rangeeH or (endeH==rangeeH and endeM<rangeeM)):#anfang out
                        start = 166
                        st = startH+(startM/60.0)
                        sr = rangeaH+(rangeaM/60.0)
                        laenge -= (sr-st)*60
                        width = laenge*(1100.0/150.0)
                        width = int(width)
                        drawble = True
                    if(drawble):
                        tempbutton = xbmcgui.ControlButton(int(start+1), y, int(width-2), 62, "", focusTexture = SKIN_PATH_BUTTON_FOCUS, noFocusTexture = SKIN_PATH_BUTTON_NOFOCUS)
                        self.addControl(tempbutton)
                        tempbutton.setVisibleCondition('[!Control.IsVisible('+str(SKIN_EPG_VISIBILITY_MARKER)+')]')  
                        if(int(width-2)<25):
                            tempbutton.setLabel("")
                        else:
                            tempbutton.setLabel(sendung["titel"])
                        self.buttons.append(tempbutton)
                        self.butnav[c-1].append(tempbutton)
                        self.buttoninfos[str(tempbutton.getId())] = [playlistidx, iterator-1]
        print "Fertig"
        self.setnavigation()
        self.show()

    def setnavigation(self):
        i = 0
        j = 0
        for sender in self.butnav:
            j=0
            for sendung in sender:
                if(i==0):
                    sendung.controlUp(self.epgviewup)
                else:
                    try:
                        sendung.controlUp(self.butnav[i-1][0])
                    except:
                        pass
                if(i==MAX_SENDER-1):
                    sendung.controlDown(self.epgviewdown)
                else:
                    #print "j: "+str(j)
                    #print "i: "+str(i) , "insgesammt: " +str(len(self.butnav))
                    #print "--------------"
                    try:
                        sendung.controlDown(self.butnav[i+1][0])
                    except:
                        pass
                if(j==0):
                    pass
                else:
                    sendung.controlLeft(self.butnav[i][j-1])
                if(j==len(self.butnav[i])-1):
                    pass
                else:
                    sendung.controlRight(self.butnav[i][j+1])      
                j += 1
            i += 1

    def drawepgInfo(self,channelid, sendungsid):
        index = channelid
        aktidx = sendungsid
        startH, startM = self.epglist[index][aktidx]["zeit"].split(":")
        startH = int(startH)
        startM = int(startM)
        laenge = self.epglist[index][aktidx]["laenge"].replace(" min.","")
        if(laenge != ''):
            laenge = int(laenge)
        else:
            laenge = 60
        endeM = startM + laenge
        n = (endeM / 60)
        endeH = startH + n
        endeM -= n*60
        dauer = str(startH).zfill(2)+":"+str(startM).zfill(2)+" - "+str(endeH).zfill(2)+":"+str(endeM).zfill(2)
        self.getControl(SKIN_EPG_TVINFO_LAENGE).setLabel(dauer)
        
        infos = "Informationen:\n"
        infos = (infos + self.epglist[index][aktidx]["genrejahr"] + "\n") if self.epglist[index][aktidx]["genrejahr"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["laenge"] + "") if self.epglist[index][aktidx]["laenge"] != "" else (infos + "")
        infos = (infos + ", " + self.epglist[index][aktidx]["FSK"] + "\n") if self.epglist[index][aktidx]["FSK"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["regie"] + "\n") if self.epglist[index][aktidx]["regie"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["drehbuch"] + "\n") if self.epglist[index][aktidx]["drehbuch"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["kamera"] + "\n") if self.epglist[index][aktidx]["kamera"] != "" else (infos + "")
        infos = (infos + self.epglist[index][aktidx]["musik"] + "\n") if self.epglist[index][aktidx]["musik"] != "" else (infos + "")
        
        self.getControl(SKIN_EPG_TVINFO_INFOS).setLabel(infos)
        self.getControl(SKIN_EPG_TVINFO_TITEL).setLabel(self.epglist[index][aktidx]["titel"])
        self.getControl(SKIN_EPG_TVINFO_UNTERTITEL).setLabel(self.epglist[index][aktidx]["episodentitel"].replace("Episodentitel: ",""))

        self.getControl(SKIN_EPG_TVINFO_BESCHREIBUNG).setLabel(self.epglist[index][aktidx]["beschreibung"])


    def onAction(self, action):
        """
            onAction in WindowXML works same as on a Window or WindowDialog its for keypress/controller buttons etc
            This function has been implemented and works
        """
        self.uhr()
        buttonCode =  action.getButtonCode()
        actionID   =  action.getId()
        #print "onAction(): actionID=%i buttonCode=%i" % (actionID,buttonCode)
        if (actionID == ACTION_MOUSE_LEFT_CLICK):
            self.show()
        if (actionID == ACTION_MOUSE_RIGHT_CLICK):
            self.show()                
        elif (actionID == ACTION_PREVIOUS_MENU):
            self.close()
        elif (buttonCode == KEY_G or actionID == ACTION_KONTEXT):
            if(self.modus == "EPG"):
                self.modus = "Full"            
            elif(self.modus == "Full"):
                self.modus = "EPG"
                self.onGuideButton()
            self.redraw()
        elif (actionID ==  ACTION_SHOW_INFO):
            if(self.info == True):
                self.hideinfo()  
                self.info = False
            elif(self.info == False):
                self.showinfo()
                self.info = True
        elif (actionID == ACTION_MOVE_LEFT and self.modus =="Full"):
            if(self.player.Index() == (self.player.Count()-1)):
                self.player.playselected(0)
            else:
                self.player.playnext()
        elif (actionID == ACTION_MOVE_RIGHT and self.modus =="Full"):
            if(self.player.Index() == 0):
                self.player.playselected((self.player.Count()-1))
            else:
                self.player.playprevious()
        elif (buttonCode == KEY_U):
            self.player.playselected(self.player.Index())
        elif (buttonCode == KEY_L):
            #Playlist
            print "test"
            xbmc.executebuiltin( "XBMC.ActivateWindow(10028)" )
            #print xbmcaddon.Addon().getAddonInfo('path')+ "\resources\skins\Default\720p\test.xml"
        elif (buttonCode == KEY_O):
            self.reloadplaylist()



        
    def onClick(self, controlID):
        """
            onClick(self, controlID) is the replacement for onControl. It gives an interger.
            This function has been implemented and works
        """
        print "onclick(): control %i" % controlID

        if (self.modus =="EPG"):
            self.player.playselected(self.buttoninfos[str(controlID)][0])
        if (controlID == 100):
            print "Some Control with id 2 was pressed"

    def onFocus(self, controlID):
        """
            onFocus(self, int controlID)
            This function has been implemented and works
        """
        if (str(controlID) in self.buttoninfos):
            self.drawepgInfo(self.buttoninfos[str(controlID)][0],self.buttoninfos[str(controlID)][1])

        if (str(controlID) == str(self.epgviewup.getId())):
            self.setFocus(self.butnav[0][0])
            if(self.navpos > 0):
                self.navpos -= 1
                self.drawallepg(self.epglist[self.navpos:self.navpos+MAX_SENDER])
            self.setFocus(self.butnav[0][0])

        if (str(controlID) == str(self.epgviewdown.getId())):
            self.setFocus(self.butnav[MAX_SENDER-1][0])
            #self.redrawEPGdown()
            if(self.navpos < len(self.playlist)-MAX_SENDER):
                self.navpos += 1
                self.drawallepg(self.epglist[self.navpos:self.navpos+MAX_SENDER])
            self.setFocus(self.butnav[MAX_SENDER-1][0])

