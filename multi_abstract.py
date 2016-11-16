#coding:utf-8

import re
import pickle
from text_feature import TextFeature
import jieba
from textrank4zh import TextRank4Sentence
import json
import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import cosine_similarity

jieba.load_userdict("user.dict")

sw = dict()
for line in open("stopwords.txt", "r"):
  sw[line.strip()] = 1
print "load stopwords: %d" % len(sw)

p_num = re.compile(r'^\d+$')
valid_chars = re.compile(ur'^[\u4e00-\u9fa5a-zA-Z0-9]+$')

text_fea    = pickle.load(open('chat_text_f.dat'))

categories = range(0,200)
category_idx_contexts = dict([(category, {}) for category in categories]) #{category:{docid:context}}
# category_contexts = dict([(category, []) for category in categories]) #{category:[context1,context2,...context7]}
category_abs = dict()

tr4s = TextRank4Sentence()

import MySQLdb
conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
cursor = conn.cursor()

sql = "select category, id,context from t_antif_article_analyze where category <> '' "
try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    for r in results:
      #print type(r[0])
      #print type(r[1])
      #print("%d %s" %(int(r[0]),r[1]))
      #print "will deal context..."
      text = r[2].strip().replace('\n',' ')
      cont = text.strip().replace('\t',' ')
      category_idx_contexts[int(r[0])][r[1]] = r[2]
      #print cont
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
print len(category_idx_contexts)


for cate in category_idx_contexts.iterkeys():
  content_list = []
  cnt = 0
  tfidf_matrix = None
  # content = ""

  docid_context_list = list(category_idx_contexts[cate].iteritems())
  print("cate:%s,docid_context_list len: %d" % (cate,len(docid_context_list)) )

  if len(docid_context_list) <= 1 :
    continue

  for docid, context in docid_context_list:
    cnt += 1
    content = context
    content_list.append(content)

    words = ""
    kw_vec = []

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
    words += " ".join(kw_vec)
    #print "words..."
    #print words

    text_vec = text_fea.Trans([kw_vec])[0]
    indptr = [0]
    indices = []
    data = []
    for idx in range(len(text_vec)):
      if text_vec[idx] != 0.0:
       indices.append(idx)
       data.append(text_vec[idx])
    indptr.append(len(indices))
    test_matrix = csr_matrix((data, indices, indptr), shape=(1, len(text_vec)))
    if cnt == 1:
      tfidf_matrix = test_matrix
    else:
      tfidf_matrix = vstack((tfidf_matrix,test_matrix))
  print tfidf_matrix.shape[0]
  dist = 1 - cosine_similarity(tfidf_matrix)
  sim_list = dist[0]
  # print sim_list

  idx_sim_list = []
  for k in range(len(sim_list)):
    data = (k,sim_list[k])
    idx_sim_list.append(data)

  # print idx_sim_list
  sim_list = list(reversed(sorted(idx_sim_list, key=lambda x: x[1])))[:10]
  print sim_list

  text = ""
  for idx, pro in sim_list:
    text +=  content_list[idx]
    text +=  "\n"

  tr4s.analyze(text=text, lower=True, source = 'all_filters')
  rs=[]
  abs = ""
  for item in tr4s.get_key_sentences(num=1):
    rs.append(item.sentence)
  abs += "".join(rs)
  print abs
  category_abs[cate] = abs

ab_list=[]
for k,v in category_abs.items():
    print "key:"+str(k)+",value:"+str(v)
    data = (v,k)
    ab_list.append(data)
sql = "update t_antif_cate_summary set abstract = %s where cate_id= %s"
cursor = conn.cursor()
cursor.executemany(sql,ab_list)
conn.commit()


cursor.close()
conn.close()
