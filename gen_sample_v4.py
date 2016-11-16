#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import re
import time
import json
import urllib
import urllib2
import time
import pickle
from text_feature import TextFeature
from get_label_words import LabelWords
import hashlib
import datetime
from multiprocessing import Process, Pool, Queue
import re

amount_pat = re.compile(r'\d+')
question_pat = re.compile(r'怎么|什么|如何|哪个|吗')

text_fea    = pickle.load(open('chat_text_f.dat'))
print "load feature done"

lw = pickle.load(open('label_words.dat'))


def Mapper(q, fn):
  fp = open(fn, "w")
  while True:
    sp = q.get(True)
    if sp is None:
      print "mapper %s done" % fn
      fp.close()
      return


    text_vec = text_fea.Trans([sp[1:]])[0]

    v = []
    idx = 1

    #print sp.cityvec
    # for sv in text_vec:
    #   if sv != 0:
    #     v.append('%d:%f' % (idx, sv))
    #   idx += 1

    for idx in range(len(text_vec) - 1):
      if text_vec[idx] != 0.0:
        v.append('%d:%f' % (idx+1, text_vec[idx]))
    # v.append('%d:%f' % (len(text_vec), text_vec[-1]))
    # v.append('%d:%f' % (int(sp[0]), float(0)) )
    v.append('%d:%f' % (len(text_vec), float(sp[0])) )
    # svm_str = "%s\n" % (" ".join(v))

    lw_vec = lw.Judge(sp[1:])
    if 1 in lw_vec:
      svm_str = "%s %s\n" % ('1', " ".join(v))
    else:
      svm_str = "%s %s\n" % ('0', " ".join(v))
    fp.write(svm_str)

q = Queue(16*10000)
jobs = []
job_cnt = 2
for i in range(job_cnt):
  p = Process(target = Mapper, args = (q, "semi_train_%d.txt" % i))
  jobs.append(p)
  p.start()

cnt = 0

for line in open(sys.argv[1], "r"):
#for line in open("words.txt", "r"):
  cnt += 1
  if cnt % 10000 == 0:
    time_str = datetime.datetime.now().isoformat()
    print "[%s]: %d" % (time_str, cnt)

  docid = line.strip().split("\t")[0]
  #print type(docid)
  words = line.strip().split("\t")[1]
  wl = words.split(" ")
  word_list = []
  word_list.append(docid)
  word_list.extend(wl)
  #print word_list
  q.put(word_list, block = True)

for _ in range(job_cnt):
  q.put(None, block = True)
for job in jobs:
  job.join()

print "load valid training sample: %d " % cnt

