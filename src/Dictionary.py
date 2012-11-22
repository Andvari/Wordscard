# -*- coding: UTF-8 -*-

'''
Created on Nov 22, 2012

@author: nemo
'''

import os
import re
import random

DICT_FILE     = "/dictionary.txt"

class Dictionary():
    def __init__(self):
        self.words          = {}
        self.translations   = {}
        self.size           = 0

        self.homedir = os.environ['HOME']
        
        try:
            dict_file = open(self.homedir + "/.Wordcards" + DICT_FILE, "a+")
            dict_file.close()
        except:
            print "Error opening local dictionary"
            os._exit(False)
        
            
        self.update()
    
    def add_term(self, term, translation):
        self.words[self.size] = term
        self.translations[term] = translation
    
    def remove_item(self, term):
        pass
    
    def show(self):
        pass
    
    def update(self):
        
        try:
            dict_file = open(self.homedir + "/Dropbox" + DICT_FILE, "rb")
            page = dict_file.read()
            save_file = open(self.homedir + "/.Wordcards" + DICT_FILE, "wb")
            save_file.write(page)
            
        except:
            dict_file = open(self.homedir + "/.Wordcards" + DICT_FILE, "rb")
            page = dict_file.read()
            
        dict_file.close()
        
        dct = {}
        dct = re.compile("(.*?)\n").findall(page)
            
        i=0
        for line in dct:
            self.words[i]                    = line [  : line.find(":") ]
            self.translations[self.words[i]] = line [ line.find(":") + 1 : ].encode("utf-8")
            i+=1
        self.size = i
    
    def get_size(self):
        return self.size
    
    def get_random_word(self):
        return self.words[random.randint(0, self.size-1)]
    
    def get_translation(self, term):
        return self.translations[term]
         
    