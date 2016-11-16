#-*- coding:utf-8 -*-

import pickle
from text_feature import TextFeature

fp = open("df.txt","w")
text_fea    = pickle.load(open('chat_text_f.dat'))

df_dict = text_fea.GetDf()

for k,v in df_dict.iteritems():
    print '%s\t%d' % (k, v)
    fp.write(k)
    fp.write("\t")
    fp.write(str(v))
    fp.write("\n")

fp.close()
