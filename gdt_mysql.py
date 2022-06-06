# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# -*- coding: utf-8 -*-
# @Time    : 2022/1/20 13:32
# @Author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @File    : gdt_mysql.py
# @Software: PyCharm


"""
是通过 record_5 中的 archid 和 f5_1_document 中的 id 关联
文件的绝对路径： concat('D:\\edoc\\docp',filepath,savefilename)
"""

import pymysql

server = '127.0.0.1'
user = 'root'
password = 'root'

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='guodiantou'
)
cursor = conn.cursor()
sql = 'SELECT filepath,savefilename,id FROM record_5 WHERE archid IN (SELECT id FROM f5_1_document WHERE temp3=3)'
cursor.execute(sql)
sql_value = cursor.fetchall()
print(sql_value)
# print(sql_value)
for i in sql_value:
    print(i[2])
    sql_path = 'D:\\edoc\\docp'+i[0]+i[1]
    print(sql_path)
cursor.close()
conn.close()