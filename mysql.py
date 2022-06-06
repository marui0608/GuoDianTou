# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# -*- coding: utf-8 -*-
# @Time    : 2022/1/20 18:17
# @Author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @File    : mysql.py
# @Software: PyCharm

import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='guodiantou'
)
cursor = conn.cursor()


# sq = "select MAX(doctype) from record_5 WHERE archid=(select id from f5_1_document limit 1)"
# cursor.execute(sq)
# sql_value = cursor.fetchall()
# print(sql_value)
# sql = "update f5_1_document set temp3=%s WHERE id=(select archid from record_5 limit 1)"
# val = (sql_value[0][0])
# cursor.execute(sql,val)
# sq = "select record_5.doctype from f5_1_document left join record_5 on f5_1_document.id = record_5.archid where f5_1_document.id = record_5.archid order by desc limit 1"

sq = "select f5_1_document.id,max(record_5.doctype) from f5_1_document left join record_5 on f5_1_document.id = record_5.archid group by record_5.archid;"
cursor.execute(sq)
sql_value = cursor.fetchall()
for sql_val in sql_value:
# sql = "update f5_1_document, record_5 set temp3=0 WHERE f5_1_document.id=record_5.archid"
    sql = "update f5_1_document join record_5 on f5_1_document.id = record_5.archid set temp3=%d where f5_1_document.id = %s"%(int(sql_val[1]),sql_val[0])

    print(sql_val[0],sql_val[1])
    cursor.execute(sql)
    conn.commit()

cursor.close()
conn.close()

# update f5_1_document join record_5 on f5_1_document.id = record_5.archid set temp3=(select record_5.doctype from record_5 left join f5_1_document on f5_1_document.id = record_5.archid order by record_5.doctype desc limit 1);
# if __name__ == '__main__':
#     SelectPath()


