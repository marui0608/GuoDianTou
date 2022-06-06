# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# -*- coding: utf-8 -*-
# @Time    : 2022/1/24 13:31
# @Author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @File    : client_gdt_limit.py
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
    sq = "select f5_1_document.id,max(record_5.doctype) from f5_1_document left join record_5 on f5_1_document.id = record_5.archid where record_5.doctype is not null and f5_1_document.temp3='500' group by record_5.archid"
    cursor.execute(sq)
    sql_value = cursor.fetchall()

    for sql_val in sql_value:
        # print(sql_val[0], sql_val[1])
        # if sql_val[0] != '':
        sql = "update f5_1_document set temp2=%s where id = (select archid from record_5 where archid=%s limit 1)"
        val = (sql_val[1], sql_val[0])
        cursor.execute(sql, val)
        conn.commit()
    cursor.close()
    conn.close()


# server = "http://101.200.233.202:9999/"
server = "http://127.0.0.1:5000"
def SendPath(path):
    url = f'{server}/PostGdt'
    b64 = base64.b64encode(open(path, 'rb').read()).decode('utf-8')
    data = {"suffix": os.path.splitext(path)[-1], 'file': b64}
    res = requests.post(url, json=data, timeout=10000).json()
    print(res)
    return res


def SelectPath(): # record_5 ---> path
    sql = "SELECT filepath,savefilename,id FROM record_5 WHERE archid IN (SELECT id FROM f5_1_document WHERE temp3='500') and doctype is null"
    cursor.execute(sql)
    sql_value = cursor.fetchall()
    for i in sql_value:
        sql_path = 'D:\\edoc\\docp' + i[0] + i[1]
        if os.path.exists(sql_path):
            Sen_level = SendPath(sql_path)
            if Sen_level['data']['result'] == "Error: No sensitive characters" or Sen_level['data']['result'] == "Error: NotFound suffix":
                save_sql = 'UPDATE record_5 SET doctype=%s WHERE id=%s'
                val = (-1, i[2])
                cursor.execute(save_sql, val)
                conn.commit()
            else:
                save_sql = 'UPDATE record_5 SET doctype=%s WHERE id=%s'
                val = (Sen_level['data']['result']['敏感等级'], i[2])
                cursor.execute(save_sql, val)
                conn.commit()
        else:
            save_sql = "UPDATE record_5 SET doctype=%s WHERE id=%s"
            val = (-2, i[2])
            cursor.execute(save_sql, val)
            conn.commit()
    SaveSenLevel()


if __name__ == '__main__':
    # SelectPath()
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/UNIS-ujgZSXWfcFbg7vx9dz14pe4Gg.txt"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/9d2026f79371abc0645a3c64e254de5.jpg"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/AutoCV部署手册-public.docx"
    # # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/P520工作站开机指南（汉龙思琪）.docx"
    # path =r"D:\edoc\docp/uploads/company1/fonds5/1642562174639608964/2022/20220119/P520工作站开机指南（汉龙思琪）1.oc"
    path = r"123.doc"
    SendPath(path)