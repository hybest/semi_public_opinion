#-*- coding:utf-8 -*-

import os
import sys
import pickle
from text_feature import TextFeature
import json
import datetime


# categories = [0,500,1]
categories = range(0,200)
# categories = range(0,int(sys.argv[2]))
category_word = dict([(category, {}) for category in categories]) #{category:{word:count}}
category_keywords = dict([(category, []) for category in categories]) #{category:[word1,word2,...word7]}
cnt = 0

# for line in open(sys.argv[1], "r"):
for line in open("hac_all_rst_final.txt", "r"):
  cnt += 1
  if cnt % 10000 == 0:
    time_str = datetime.datetime.now().isoformat()
    print "[%s]: %d" % (time_str, cnt)

  line_list = line.strip().split(" ")
  label = int(line_list[0])

  word_list = line_list[3:]
  #print word_list

  for word in word_list:
      # print word
      if not category_word[label].has_key(word):
        category_word[label][word] = 1
      else:
        category_word[label][word] += 1


fn = "keywords_freq.txt"
#fn = "keywords_3.txt"
with open(fn, 'w') as fo:
  fo.writelines("word\tfreq\tlabel\n")
  for label in category_word.iterkeys():
    print label
    # print len(list(reversed(sorted(list(category_word[label].iteritems()), key=lambda x: x[1]))))
    words_list = list(reversed(sorted(list(category_word[label].iteritems()), key=lambda x: x[1])))[:7]
    print len(words_list)
    #print words_list
    word_freq_cat = []
    kwl = []
    for word, freq in words_list:
      word_freq_cat.append('{0}\t{1}\t{2}\n'.format(word, freq, label))
      kwl.append(word)
    fo.writelines(word_freq_cat)
    category_keywords[label] = kwl
    # print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"

# print json.dumps(category_keywords, ensure_ascii=False, indent=2,encoding='utf8')

import MySQLdb
conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
cursor = conn.cursor()

sql = "delete from t_antif_cate_summary"
cursor.execute(sql)
conn.commit()

kw_list = []
for label in category_keywords.iterkeys():
  kl = category_keywords[label]
  keywords =""
  keywords += " ".join(kl)
  data = ( label,keywords)
  kw_list.append(data)


cursor.executemany('insert into t_antif_cate_summary(cate_id,keywords) values(%s,%s)',kw_list)
conn.commit()

cursor.close()
conn.close()
