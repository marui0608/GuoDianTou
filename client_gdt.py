# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# -*- coding: utf-8 -*-
# @Time    : 2022/1/20 14:48
# @Author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @File    : client_gdt.py
# @Software: PyCharm
import os
import base64
import requests
import pymysql


# aliyun
# conn = pymysql.connect(
#     host='101.200.233.202',
#     port=3307,
#     user='root',
#     password='guodiantou',
#     database='gdt'
# )
# cursor = conn.cursor()

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='guodiantou'
)
cursor = conn.cursor()


def SaveSenLevel():
    sq = "select f5_1_document.id,max(record_5.doctype) from f5_1_document left join record_5 on f5_1_document.id = record_5.archid group by record_5.archid;"
    cursor.execute(sq)
    sql_value = cursor.fetchall()
    for sql_val in sql_value:
        sql = "update f5_1_document join record_5 on f5_1_document.id = record_5.archid set temp3=%d where f5_1_document.id = %s"%(int(sql_val[1]),sql_val[0])
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# server = "http://101.200.233.202:9999/"
server = "http://127.0.0.1:5000"
def SendPath(path):
    url = f'{server}/PostGdt'
    b64 = base64.b64encode(open(path, 'rb').read()).decode('utf-8')
    data = {"suffix": os.path.splitext(path)[-1], 'file': b64}
    res = requests.post(url, json=data, timeout=900).json()
    return res


def SelectPath(): # record_5 ---> path
    sql = 'SELECT filepath,savefilename from record_5'
    cursor.execute(sql)
    sql_value = cursor.fetchall()
    for i in sql_value:
        sql_path = 'D:\\edoc\\docp' + i[0] + i[1]
        print(sql_path)
        Sen_level = SendPath(sql_path)
        print(Sen_level)
        if Sen_level['data']['result'] == "Error: No sensitive characters" or Sen_level['data']['result'] == "Error: NotFound suffix":
            save_sql = 'UPDATE record_5 SET doctype=null WHERE filepath=%s and savefilename=%s'
            val = (i[0], i[1])
            cursor.execute(save_sql, val)
            conn.commit()
        else:
            save_sql = 'UPDATE record_5 SET doctype=%s WHERE filepath=%s and savefilename=%s'
            val = (Sen_level['data']['result']['敏感等级'], i[0], i[1])
            cursor.execute(save_sql, val)
            conn.commit()
    SaveSenLevel()


if __name__ == '__main__':
    print(121111)
    SelectPath()
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/UNIS-ujgZSXWfcFbg7vx9dz14pe4Gg.txt"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/9d2026f79371abc0645a3c64e254de5.jpg"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/AutoCV部署手册-public.docx"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/P520工作站开机指南（汉龙思琪）.docx"
    # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/P520工作站开机指南（汉龙思琪）1.oc"
    # SendPath(path)