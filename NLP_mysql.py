# -*- coding: utf-8 -*-
# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# @author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @file    : NLP_mysql.py
# @time    : 2022/2/2418:52
# @Software: PyCharm

import pymysql
import os


conn = pymysql.connect(
    host='10.80.51.98',
    port=3306,
    user='root',
    password='ziguangruanjian',
    database='thams'
)
cursor = conn.cursor()

sql = "SELECT archid,filepath,savefilename FROM record_5 WHERE archid IN (SELECT id FROM f5_1_document WHERE temp3='500')"
cursor.execute(sql)
sql_value = cursor.fetchall()
def SqlFiles():
    result = []
    for sq in sql_value:
        if "正文" in sq[2]:
            # print(sq)
        # if os.path.splitext(sq[2])[-1] in [".pdf", ".PDF", ".doc", ".docx"] and "处理单" not in sq[2] and "附件" not in sq[2]:
            result.append(sq)
    return result

SqlFiles()
