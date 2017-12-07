# -*- coding: UTF-8 -*-

"""
Created on Nov 22, 2012

@author: nemo
"""

import os
import random

DICT_FILE = "dictionary.txt"


class Dictionary:
    def __init__(self):
        self.dict = {}
        self.dict_path = ""

        if os.path.exists(DICT_FILE):
            self.dict_path = DICT_FILE
        elif os.path.exists(os.environ['HOME'] + "/Dropbox/" + DICT_FILE):
            self.dict_path = os.environ['HOME'] + "/Dropbox/" + DICT_FILE
        else:
            print("No dictionary file found")
            exit(1)
        self.update()

    def update(self):
        with open(self.dict_path, "r") as dict_file:
            for line in dict_file:
                term = {}
                line = line.replace("\n", "")
                term['value'] = line[: line.find(":")]
                term['translation'] = line[line.find(":")+1: line.rfind(":")]
                if not term['translation']:
                    term['translation'] = " "
                term['example'] = line[line.rfind(":")+1:]
                if not term['example']:
                    term['example'] = " "
                self.dict[term['value']] = term

    def get_random_word(self):
        return self.dict[self.dict.keys()[random.randint(0, len(self.dict)-1)]]
