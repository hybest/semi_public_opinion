#-*- coding:utf-8 -*-

import MySQLdb
from textrank4zh import TextRank4Sentence

conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
# cursor = conn.cursor()

i=0
ab_list=[]
for line in open("all_cont.txt", "r"):
#for line in open("test.txt", "r"):
    text =  line.strip()
    idx =  int(text.split('\t')[0])
    # print idx
    content = text.split('\t')[1].replace('-','')
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=content, lower=True, source = 'all_filters')
    rs=[]
    abs = ""
    for item in tr4s.get_key_sentences(num=1):
        rs.append(item.sentence)
    abs += "".join(rs)
    print idx
    data = (abs,idx)
    ab_list.append(data)

    # sql = "UPDATE t_antif_article_analyze SET abstract= '"+ abs +"'  where id= '"+str(idx)+"' "
    sql = "update t_antif_article_analyze set abstract = %s where id= %s"
    if i>100:
        cursor = conn.cursor()
        cursor.executemany(sql,ab_list)
        # cursor.execute(sql)
        conn.commit()
        print("update")
        i=0
        ab_list = []
    i += 1

if i>0:
    cursor = conn.cursor()
    cursor.executemany(sql,ab_list)
    conn.commit()

cursor.close()
conn.close()

