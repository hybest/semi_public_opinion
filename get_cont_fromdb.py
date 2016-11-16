#-*- coding:utf-8 -*-

import MySQLdb
import sys

if len(sys.argv) < 3:
    print("please use %s begintime endtime such as (exec 20160901 20160903)" %sys.argv[0])
    exit(1)

print len(sys.argv)

begintime = sys.argv[1]
endtime = sys.argv[2]

fw = open('doc_idx.txt', 'w')
fd = open('all_cont.txt','w')

conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
cursor = conn.cursor()

# sql = "SELECT id,context FROM t_antif_article_analyze where publish_time='"+docname+"'"
sql = "select id,orig_key,context from t_antif_article_analyze where publish_time >= '"+begintime+"' and publish_time <= '"+endtime+"' "

try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    for r in results:
      #print("%d %s" %(r[0],r[1])) 
      #print "will deal context..."
      text = r[2].strip().replace('\n',' ')
      cont = text.strip().replace('\t',' ')
      if len(cont.encode('utf8') ) >= 20 :
        fw.write(str(r[0]) + ' ' + r[1] + "\n")
        fd.write(str(r[0]) + '\t' + cont.encode('utf8') + "\n")
      #print cont
except:
    print "Error: unable to fecth data"

cursor.close()
conn.close()
fw.close()
fd.close()
