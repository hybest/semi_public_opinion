#-*- coding:utf-8 -*-

import pickle
from get_label_words import LabelWords

lw = pickle.load(open('label_words.dat'))
print "load label words done"

lw.Dump()

