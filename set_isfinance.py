#-*- coding:utf-8 -*-

import MySQLdb

conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
cursor = conn.cursor()

i=0

for line in open("positive_docid.txt", "r"):
#for line in open("test.txt", "r"):
    docid =  line.strip()
    sql = "update t_antif_article_analyze set is_finance = 1 where id='"+docid+"'"
    cursor.execute(sql)
    conn.commit()
print("update")
cursor.close()
conn.close()
