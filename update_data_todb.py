#-*- coding:utf-8 -*-

sw = dict()
for line in open("filter.txt", "r"):
  sw[line.strip()] = 1
print "load filterwords: %d" % len(sw)

cnt = 0
categories = range(0,200)
cate_data_count = dict([(category,0) for category in categories]) #category:data_count
for line in open("hac_all_rst_final.txt", "r"):
  line_list = line.strip().split(" ")
  label = int(line_list[0])
  cate_data_count[label] += 1
  cnt += 1

print("cnt:%d \n" %cnt)
  # keyword_list = line_list[3:]

for k,v in cate_data_count.items():
    # print "key:"+str(k)+",value:"+str(v)
    p = float(v/float(cnt))
    print p
    if p < 0.001:
        del cate_data_count[k]

print len(cate_data_count)
print cate_data_count

import MySQLdb
conn = MySQLdb.connect(host='10.130.81.130', port=3306, user='root', passwd='root', db='antif',charset="utf8")
cursor = conn.cursor()

for line in open("hac_all_rst_final.txt", "r"):
#for line in open("hac_result.txt", "r"):
  keywords =""
  line_list = line.strip().split(" ")
  label = int(line_list[0])
  #print label
  if label not in cate_data_count.keys():
      print label
      continue

  itemid = line_list[1]
  docname = line_list[2]
  #print docname
  keyword_list = line_list[3:]
  flag = False

  for kw in keyword_list:
      if sw.has_key(kw):
          print("%s in filter word list" %kw)
          flag = True
          break
  print flag
  if flag == False :
    keywords += " ".join(keyword_list)
    #print keywords
    sql = "UPDATE t_antif_article_analyze SET category= '"+ str(label) +"' , key_word= '"+ keywords +"' where id='"+itemid+"'"
    cursor.execute(sql)
    conn.commit()
    # SQL 查询语句
    # sql = "SELECT id FROM t_antif_article_analyze where orig_key='"+docname+"'"
    # try:
    #  # 执行SQL语句
    #   cursor.execute(sql)
    #  # 获取所有记录列表
    #   result = cursor.fetchone()
    #   print result
    #   if result == None:
    #     pass
    #     #print "This data is not in the table..."
    #     # sql = "insert into t_antif_article_analyze(orig_key,category,key_word) values('"+docname+"' , '"+ str(label) +"' , '"+keywords+"')"
    #     # cursor.execute(sql)
    #     # conn.commit()
    #   else:
    #     print keywords
    #     sql = "UPDATE t_antif_article_analyze SET category= '"+ str(label) +"' , key_word= '"+ keywords +"' where orig_key='"+docname+"'"
    #     cursor.execute(sql)
    #     conn.commit()
    # except:
    #   print "Error: unable to fecth data"

cursor.close()
conn.close()
