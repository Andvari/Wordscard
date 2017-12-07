#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Created on Nov 20, 2012

@author: nemo
"""

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
            self.status = "Already run"
            print("Application already run")
            return
        except:
            self.status = "Stopped"

        DBusGMainLoop(set_as_default=True)
        dbus.service.Object.__init__(self, dbus.service.BusName('home.nemo.Wordcards', dbus.SessionBus()), '/home/nemo/Wordcards')

        self.is_learning = 0
        self.config = {'timeout': '120'}
        self.home_dir = os.environ['PWD']
        self.menu = gtk.Menu()

        assert os.path.exists(self.home_dir + "/config"), "Wordcards does not properly installed"
        assert os.path.exists(self.home_dir + "/images/word_on.png"), "Wordcards does not properly installed"
        assert os.path.exists(self.home_dir + "/images/word_off.png"), "Wordcards does not properly installed"

        self.read_cfg()
        self.tmr = threading.Timer(int(self.config['timeout']), self.on_timer)

        self.ind = appindicator.Indicator("hello world client", "", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        
        self.ind.set_icon_theme_path(self.home_dir + "/images")
        self.ind.set_icon("word_off")

        self.dict = Dictionary.Dictionary()
        self.kb = Numpad.Numpad()
        self.kb.connect("z_signal", self.on_z_signal)

        self.make_menu()

    def make_menu(self):
        self.menu.destroy()
        self.menu = gtk.Menu()

        item_runstop = gtk.MenuItem()
        item_runstop.add(gtk.Label(self.status))
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

        item_mode = gtk.MenuItem()
        if self.is_learning:
            item_mode.add(gtk.Label("Listening mode"))
        else:
            item_mode.add(gtk.Label("Learning mode"))

        self.menu.append(item_mode)
        item_mode.show()
        item_mode.connect("activate", self.on_mode)

        item_edit = gtk.MenuItem()
        item_edit.add(gtk.Label("Update dictionary"))

        self.menu.append(item_edit)
        item_edit.show()
        item_edit.connect("activate", self.dict.update)

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
        if self.status == "Runned":
            if self.dict:
                term = self.dict.get_random_word()
                if self.is_learning == 0:
                    n = pynotify.Notification(term['value'], term['translation'], "Null")
                    #os.system("echo " + term['value'] + "| festival --tts ; sleep 2")
                    os.system("spd-say -r -70 \"" + term['value'] + "\" ; sleep 2")
                    os.system("echo " + term['translation'] + "| festival --tts --language russian ; sleep 1" )
                    #os.system("echo " + term['example'] + "| festival --tts")
                    if len(term['example']) > 0:
                        os.system("spd-say -r -70 \"" + term['example'] + "\"")
                else:
                    n = pynotify.Notification (term['value'], "", "Null")
                    #os.system("echo " + term['value'] + "| festival --tts")
                    os.system("spd-say -r -70\"" + term['value'] + "\"")
                n.show()
        self.tmr = threading.Timer(int(self.config['timeout']), self.on_timer)
        self.tmr.start()

    def on_runstop(self, e):
        if self.status == "Runned":
            self.tmr.cancel()
            self.status = "Stopped"
            self.ind.set_icon("word_off")
        else:
            self.status = "Runned"
            self.ind.set_icon("word_on")
            self.tmr.start()
        self.make_menu()

    def on_timeout(self, e):
        self.kb.show_all()

    def on_mode(self, e):
        self.is_learning = 1 - self.is_learning
        self.make_menu()

    def on_quit(self, e):
        self.write_cfg()
        self.tmr.cancel()
        gtk.main_quit()
        
    def on_z_signal(self, e, state):
        if state:
            self.config['timeout'] = self.kb.get_text_to_find()
            if int(self.config['timeout']) > 3600:
                self.config['timeout'] = '3600'
            self.tmr.cancel()
            self.tmr = threading.Timer(int(self.config['timeout']), self.on_timer)
        self.kb.hide_all()
        self.make_menu()
        
    def read_cfg(self):
        with open(self.home_dir + "/config", "r") as cfg:
            for line in cfg:
                line = line.replace("\n", "")
                name = line[: line.find("=")]
                value = line[line.find("=")+1:]
                self.config[name] = value

    def write_cfg(self):
        with open(self.home_dir + "/config", "w") as cfg:
            for line in self.config:
                cfg.write(line + "=" + self.config[line] + "\n")

if Wordcards().status != "Already run":
    gtk.gdk.threads_init()
    gtk.main()

exit(0)
