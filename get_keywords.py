#coding=utf-8

import os
import sys
sys.path.append("/home/minghaiyan/thirdparty/jieba-master")
#import jieba.analyse
import re
import time
import datetime
import pickle
import jieba
import jieba.analyse
jieba.load_userdict("user.dict")

sw = dict()
for line in open("stopwords.txt", "r"):
  sw[line.strip()] = 1
print "load stopwords: %d" % len(sw)

p_num = re.compile(r'^\d+$')
valid_chars = re.compile(ur'^[\u4e00-\u9fa5a-zA-Z0-9]+$')

fp = open("keywords.txt","w")
cnt = 0
for line in open(sys.argv[1], "r"):
# for line in open("suspect_phone_number.txt", "r"):
  cnt += 1
  if cnt % 1000 == 0:
    time_str = datetime.datetime.now().isoformat()
    print "[%s]: %d" % (time_str, cnt)

  # parts = json.dumps(line.strip())
  # print parts

  words = ""
  kw_vec = []
  # decodejson = json.loads(line.strip() )
  # print type(decodejson)
  print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  content = line.strip()
  # content =  ''.join([x for x in decodejson['self']['msg'] if x != " "])
  # content =  ''.join([x for x in line.strip() if x != " "])
  # print content

  print "------------------------------------"

  for t in jieba.cut(content):
    if valid_chars.match(t) is None:
      continue
    t = t.lower()

    tl = t.strip().encode('utf8')
    if (not tl) or sw.has_key(tl):
      continue
    if p_num.match(tl):
      continue
    kw_vec.append(tl)
  # word_vec.append(kw_vec)

  # print kw_vec
  words += " ".join(kw_vec)
  # print "words..."
  # print words
  topK = 5
  tags = jieba.analyse.extract_tags(words, topK=topK)
  print ",".join(tags)
  keywords = " ".join(tags)
  if len(tags) > 0 :
    fp.write(keywords.encode('utf8') + "\n")

fp.close()

