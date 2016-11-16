#-*- coding:utf-8 -*-

import pickle
from text_feature import TextFeature

fp = open("vocab.txt","w")
text_fea    = pickle.load(open('chat_text_f.dat'))

vocab_dict = text_fea.GetVocab()

for k,v in vocab_dict.iteritems():
    print '%s\t%d' % (k, v)
    fp.write(k)
    fp.write("\t")
    fp.write(str(v))
    fp.write("\n")

fp.close()
