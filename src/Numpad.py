# -*- coding: UTF-8 -*-
import gtk
import os
import pango
import gobject

MULT = 1

KB_COLS = 13
KB_ROWS = 1

buttons_ru = [ "ESC", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "BACKSP", "GO"] 


class Numpad(gtk.Window):
    
    def __init__(self):
        super(Numpad, self).__init__()
        
        self.flag = 0
        self.text = ""
        
        pangoFont = pango.FontDescription("Tahoma 24.2")

        try:
            gobject.signal_new("z_signal", self, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN, ))
        except:
            pass

        self.set_decorated(False)
        
        self.modify_font(pangoFont)
        
        self.set_title("Set timeout")
        
        self.tb = gtk.TextBuffer()
        self.tb.set_text("Set timeout")
        
        self.set_default_size(MULT*160, MULT*90)

        self.tv = gtk.TextView(self.tb)
        self.tv.modify_font(pangoFont)
        
        self.tv.set_editable(False)
        self.tv.set_border_width(3)

        self.vbox  = gtk.VBox()
        self.vbox.add(self.tv)

        self.hbox = {}
        for i in range(KB_ROWS):
            self.hbox[i] = gtk.HBox()
            for j in range(KB_COLS):
                self.button = gtk.Button(label = buttons_ru[i*KB_COLS+j])
                self.button.connect("clicked", self.on_click, i*KB_COLS+j)
                self.hbox[i].add(self.button)
            self.vbox.add(self.hbox[i])

        self.add(self.vbox)
        self.set_position(gtk.WIN_POS_CENTER)
        
    def on_click(self, e, prm):
        if(self.flag == 0):
            self.tb.delete(self.tb.get_start_iter(), self.tb.get_end_iter())
        
        if (buttons_ru[prm] == "BACKSP"):
            start = self.tb.get_end_iter()
            end   = self.tb.get_end_iter()
            start.backward_char()
            self.tb.delete(start, end)
        elif (buttons_ru[prm] == "GO"):
            self.flag = 0
            self.emit("z_signal", True)
        elif (buttons_ru[prm] == "ESC"):
            self.flag = 0
            self.emit("z_signal", False)
        else:
            self.tb.insert(self.tb.get_end_iter(), buttons_ru[prm])
            self.flag = 1
            
    def get_text_to_find(self):
        self.text = self.tb.get_text(self.tb.get_start_iter(), self.tb.get_end_iter())
        try:
            self.text = str(int(self.text))
        except:
            self.text = '120'

        print self.text
        return self.text
   
