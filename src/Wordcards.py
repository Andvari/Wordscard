#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Created on Nov 20, 2012

@author: nemo
'''

import os
import gtk
import appindicator
import pynotify
import threading
import random
import re
import Numpad

class Wordcards():

    def __init__(self):
        self.state = "Stopped"
        self.interval = 60
            
        self.ind = appindicator.Indicator("hello world client", "", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        
        self.ind.set_icon_theme_path("home/nemo/workspace/Wordcards/src/images")
        self.ind.set_icon("word_off")

        self.dict_size = 0
        try:
            fl = open("dictionary.txt", "r")
            page = fl.read()
            
            dct = {}
            dct = re.compile("(.*?)\n").findall(page)
            
            i=0
            self.word = {}
            self.transl = {}
            for line in dct:
                self.word[i]              = line [  : line.find(":")]
                self.transl[self.word[i]] = line [ line.find(":") + 1 : ].encode("utf-8")
                i+=1
            self.dict_size = i
            
        except:
            pass
        
        self.kb = Numpad.Numpad()
        self.kb.connect("z_signal", self.on_z_signal)

        self.makeMenu()
            
    def makeMenu(self):
        self.menu = gtk.Menu()
       
        item_runstop = gtk.MenuItem()
        item_runstop.add(gtk.Label(self.state))
        self.menu.append(item_runstop)
        item_runstop.show()
        item_runstop.connect("activate", self.on_runstop)

        item = gtk.SeparatorMenuItem()
        self.menu.append(item)
        item.show()
        
        item_interval = gtk.MenuItem()
        item_interval.add(gtk.Label("Set interval  [ " + str(self.interval) + " ]"))
        self.menu.append(item_interval)
        item_interval.show()
        item_interval.connect("activate", self.on_interval)

        item_edit = gtk.MenuItem()
        item_edit.add(gtk.Label("Edit dictionary"))
        self.menu.append(item_edit)
        item_edit.show()
        item_edit.connect("activate", self.on_edit)

        item = gtk.SeparatorMenuItem()
        self.menu.append(item)
        item.show()
        
        item_quit = gtk.MenuItem()
        item_quit.add(gtk.Label("Quit"))
        self.menu.append(item_quit)
        item_quit.show()
        item_quit.connect("activate", self.on_quit)
            
        self.ind.set_menu(self.menu)
        
        pynotify.init("Null")
        
    def on_timer(self):
        if (self.state == "Runned"):
            if (self.dict_size > 0):
                i = random.randint(0, self.dict_size-1)
                n = pynotify.Notification (self.word[i], self.transl[self.word[i]], "Null")
                n.show ()
                    
        self.tmr = threading.Timer(self.interval, self.on_timer)
        self.tmr.start()
                        
    def on_runstop(self, e):
        if (self.state == "Runned"):
            self.state = "Stopped"
            self.ind.set_icon("word_off")
        else:
            self.state = "Runned"
            self.ind.set_icon("word_on")
            self.tmr = threading.Timer(self.interval, self.on_timer)
            self.tmr.start()
                        
            
        self.makeMenu()

    def on_edit(self, e):
        pass

    def on_interval(self, e):
        self.kb.show_all()

    def on_quit(self, e):
        gtk.main_quit()
        
    def on_z_signal(self, e):
        self.interval = self.kb.get_text_to_find()
        if(self.interval > 3600):
            self.interval = 3600
        self.kb.hide()
        self.makeMenu()        
        
wc = Wordcards()
gtk.gdk.threads_init()
gtk.main()
    
os._exit(0)

