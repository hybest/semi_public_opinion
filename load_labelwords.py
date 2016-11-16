#coding=utf-8

from get_label_words import LabelWords
import pickle

lw = LabelWords()
lw.Build("labelcfg.txt")
pickle.dump(lw, open("label_words.dat", "w"))

