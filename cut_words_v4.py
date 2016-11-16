#coding=utf-8

import os
import sys
import json
sys.path.append("/home/minghaiyan/thirdparty/jieba-master")
import re
import time
import datetime
import pickle
import jieba
import jieba.analyse
jieba.load_userdict("user.dict")
from text_feature import TextFeature
from get_label_words import LabelWords
from multiprocessing import Process, Pool, Queue


#### input is other train material ####
sw = dict()
for line in open("stopwords.txt", "r"):
  sw[line.strip()] = 1
print "load stopwords: %d" % len(sw)

p_num = re.compile(r'^\d+$')
valid_chars = re.compile(ur'^[\u4e00-\u9fa5a-zA-Z0-9]+$')
# print " ".join(jieba.lcut("要依法利用社会集资来做"))

lw = LabelWords()
lw.Build("labelcfg.txt")
pickle.dump(lw, open("label_words.dat", "w"))

def BuildJob(q, fn, cs):
  f = TextFeature()
  cache = []
  cnt = 0

  while True:
    r = q.get(True)
    cnt += 1
    if cnt % 10000 == 0:
      print "build %s: %d" % (fn, cnt)

    if r is None:
      if len(cache) > 0:
        f.Build(cache)
        cache = []
      if fn == 'chat_text_f.dat':
        print "prune..."
        f.Prune(3, 3)
      pickle.dump(f, open(fn, "w"))
      print "feature build %s succ" % fn
      return
    else:
      cache.append(r)
      if len(cache) >= cs:
        f.Build(cache)
        cache = []


q_norm = Queue(10*10000)
jobs = []


p = Process(target = BuildJob, args = (q_norm, "chat_text_f.dat", 100))
jobs.append(p)
p.start()

# word_vec =[]
fp = open("chat_words.txt","w")
fk = open("chat_keywords.txt","w")
cnt = 0

#for line in open(sys.argv[1], "r"):
for line in open("all_cont.txt", "r"):
  cnt += 1
  if cnt % 1000 == 0:
    time_str = datetime.datetime.now().isoformat()
    print "[%s]: %d" % (time_str, cnt)

  # parts = json.dumps(line.strip())
  # print parts

  words = ""
  keywords = ""
  kw_vec = []
  #print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  # content =  ''.join([x for x in line.strip()  if x != " "])
  text =  line.strip()
  idx =  int(text.split('\t')[0])
  # print idx
  content = text.split('\t')[1]
  # print content

  #print "------------------------------------"

  for t in jieba.cut(content):
    if valid_chars.match(t) is None:
      continue
    t = t.lower()

    tl = t.strip().encode('utf8')
    if (not tl) or sw.has_key(tl):
      continue
    if p_num.match(tl):
      continue
    if len(tl.decode('utf8')) < 2:
      continue
    kw_vec.append(tl)
    # print("word:%s, word len: %d" %(tl,len(tl.decode('utf8'))))
  # word_vec.append(kw_vec)
  q_norm.put(kw_vec)

  # print kw_vec
  words += " ".join(kw_vec)
  if len(kw_vec) > 0 :
    fp.write(str(idx).encode("utf8") + "\t" + words + "\n")
  # print "words..."
  # print words
  topK = 7
  tags = jieba.analyse.extract_tags(words, topK=topK)
  #print ",".join(tags)
  keywords += " ".join(tags)
  if len(tags) > 0 :
    fk.write(str(idx) + "\t" + keywords.encode("utf8") + "\n")
fp.close()
fk.close()
q_norm.put(None)
for job in jobs:
  job.join()

print "dump text feature succ"
os._exit(-1)
