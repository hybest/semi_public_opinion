#coding:utf-8

#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import json
import ConfigParser

class LabelWords(object):
    def __init__(self):
        self.labelwords_map = dict()
        self.words_list = []
        self.label_number = 0

    def Dump(self):
        print json.dumps(self.labelwords_map, ensure_ascii=False, indent=2,encoding='utf8')

    ### v is like ['a', 'b', 'a', 'b']
    def Build(self, configFile):
        cfg = ConfigParser.ConfigParser()
        cfg.read(configFile)

        loan_words = cfg.get('label', 'loan')
        words = loan_words.split(',')
        for word in words:
            self.labelwords_map[word] = int(1)
            self.words_list.append(word)

        tech_words = cfg.get('label', 'tech')
        words = tech_words.split(',')
        for word in words:
            self.labelwords_map[word] = int(1)
            self.words_list.append(word)

        industry_words = cfg.get('label', 'finance')
        words = industry_words.split(',')
        for word in words:
            self.labelwords_map[word] = int(1)
            self.words_list.append(word)
        self.label_number = len(self.labelwords_map)


    def Judge(self, vl):
        rvs = []
        for v in vl:
            rst = self.labelwords_map.get(v)
            if rst == None:
                rst = 0
            rvs.append(rst)
        return rvs

    def Check(self, vl):
        rvs = {}
        for v in vl:
            rst = self.labelwords_map.get(v)
            if rst == None:
                rst = 0
            rvs[v] = rst
        return rvs
