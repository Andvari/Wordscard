# -*- coding: UTF-8 -*-

'''
Created on Nov 22, 2012

@author: nemo
'''

import os
import random

DICT_FILE     = "/dictionary.txt"

class Dictionary():
    def __init__(self):
        self.dict = {}
        self.size = 0

        self.homedir = os.environ['HOME']
        
        try:
            dict_file = open(self.homedir + "/.Wordcards" + DICT_FILE, "a+")
            dict_file.close()
        except:
            print "Error opening local dictionary"
            os._exit(False)
        
            
        self.update()
    
    def add_term(self, term, translation):
        try:
            self.dict[term]
        except:
            self.dict[term] = translation
    
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
            save_file.close()
            dict_file.close()
        except:
            pass
            
        dict_file = open(self.homedir + "/.Wordcards" + DICT_FILE, "r")

        for line in dict_file:
            line = line.replace("\n", "")
            term = line[ : line.find(":")]
            translate = line[ line.find(":")+1 : ]
            self.dict[term] = translate
        self.size = len(self.dict.keys())
        
        dict_file.close()
        
    
    def get_size(self):
        return self.size
    
    def get_random_word(self):
        return self.dict.keys()[random.randint(0, self.size-1)]
    
    def get_translation(self, term):
        return self.dict[term]
         
    