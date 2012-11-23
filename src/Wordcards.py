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
import Numpad
import Dictionary
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

class Wordcards(dbus.service.Object):
    def __init__(self):
        try:
            DBusGMainLoop(set_as_default=True)
            dbus.SessionBus().get_object('home.nemo.Wordcards', '/home/nemo/Wordcards')
            self.status = 1
            print "Application already works"
            return
        except:
            self.status = 0
        
        DBusGMainLoop(set_as_default=True)
        dbus.service.Object.__init__(self, dbus.service.BusName('home.nemo.Wordcards', dbus.SessionBus()), '/home/nemo/Wordcards')

        self.counter = 0
        self.is_learning = 0
        self.state = "Stopped"
        self.config = {}
        
        self.homedir = os.environ['HOME']
        
        try:
            os.mkdir(self.homedir + "/.Wordcards")
        except:
            pass
        
        cfg = open(self.homedir + "/.Wordcards/config", "a+")
        cfg.close()
        
        self.read_cfg()
        
        self.ind = appindicator.Indicator("hello world client", "", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        
        try:
            open(self.homedir + "/.Wordcards/images/word_off.png",  "r")
            open(self.homedir + "/.Wordcards/images/word_on.png", "r")
        except:
            print "Icons not found"
            os._exit(False)
            
        self.ind.set_icon_theme_path(self.homedir + "/.Wordcards/images")
        self.ind.set_icon("word_off")

        self.dict = Dictionary.Dictionary()
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
        
        item_timeout = gtk.MenuItem()
        item_timeout.add(gtk.Label("Set timeout  [ " + self.config['timeout'] + "s ]"))
        self.menu.append(item_timeout)
        item_timeout.show()
        item_timeout.connect("activate", self.on_timeout)

        item_edit = gtk.MenuItem()
        item_edit.add(gtk.Label("Update dictionary"))
        self.menu.append(item_edit)
        item_edit.show()
        item_edit.connect("activate", self.on_update)

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
            if (self.dict.get_size() > 0):
                term = self.dict.get_random_word()
                translation = self.dict.get_translation(term)
                if (self.is_learning == 0): 
                    n = pynotify.Notification (term, translation, "Null")
                else:
                    n = pynotify.Notification (term, "", "Null")
                n.show ()
                self.counter += 1
                if(self.counter > self.dict.get_size()):
                    self.is_learning = 1 - self.learning
                    self.counter = 0
                    
        self.tmr = threading.Timer(int(self.config['timeout']), self.on_timer)
        self.tmr.start()
                        
    def on_runstop(self, e):
        if (self.state == "Runned"):
            self.tmr.cancel()
            self.state = "Stopped"
            self.ind.set_icon("word_off")
        else:
            self.state = "Runned"
            self.ind.set_icon("word_on")
            self.tmr = threading.Timer(int(self.config['timeout']), self.on_timer)
            self.tmr.start()
        self.makeMenu()

    def on_update(self, e):
        self.dict.update()

    def on_timeout(self, e):
        self.kb.show_all()

    def on_quit(self, e):
        self.write_cfg()
        gtk.main_quit()
        
    def on_z_signal(self, e, state):
        if (state == True):
            self.config['timeout'] = self.kb.get_text_to_find()
            if(int(self.config['timeout']) > 3600):
                self.config['timeout'] = '3600'
                
        self.kb.hide_all()
        self.makeMenu()
        
        
    def read_cfg(self):
        cfg = open(self.homedir + "/.Wordcards/config", "r")
        for line in cfg:
            line = line.replace("\n", "")
            name = line[ : line.find("=")]
            value = line[ line.find("=")+1 : ]
            self.config[name] = value
        
        try:
            int(self.config['timeout'])
        except:
            self.config['timeout'] = '120'
            
        cfg.close()
        
    def write_cfg(self):
        cfg = open(self.homedir + "/.Wordcards/config", "w")
        for line in self.config:
            cfg.write(line + "=" + self.config[line] + "\n")
            
        cfg.close()
        
wc = Wordcards()
if (wc.status == 0):
    gtk.gdk.threads_init()
    gtk.main()
    
os._exit(0)

