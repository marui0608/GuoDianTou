# -*- coding: utf-8 -*-
# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# @author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @file    : NLP_Test.py
# @time    : 2022/2/2418:52
# @Software: PyCharm


import os
import docx
from ocr import api_call
from filereader import FILEREADER
from NLP_mysql import SqlFiles
import subprocess
import pandas as pd


file_reader_engine = 'http://10.80.49.137:80/service/'
ocr_server = "http://10.80.49.137:8507"
scene = "chinese_print"

def xw_toExcel(data, ID):
    fileName = "/root/GuoDianTou/Nlps_2022517.xlsx"
    rb = pd.read_excel(io=fileName, sheet_name="Sheet1", dtype={'ID':str})
    rb.loc[rb.ID==str(ID), 'Content'] = data
    rb.to_excel(fileName)




def Identification(file_path, ID):
    file = open(file_path, "r", encoding="utf-8", errors='ignore')
    content = file.read()
    file.close()
    msg = "".join(content).replace("\n", "").replace(" ", "").replace("（","(").replace("）", ")")
    msgs = msg.split('。')[0:3]
    ms = "".join(msgs)
    xw_toExcel(ms, ID)


def Doc_Ident(file_path, ID):
    try:
        output = subprocess.check_output(["antiword", file_path])
        # 解码
        output = output.decode("utf8")
        outputs = output.split('。')[0:3]
        ou = "".join(outputs)
        xw_toExcel(ou, ID)
    except Exception as subprocess_CalledProcessError:
        print(subprocess_CalledProcessError)

def Docx_Ident(file_path, ID):
    content = ""
    try:
        document = docx.Document(file_path)
        for paragraph in document.paragraphs:
            content += paragraph.text
        msg = ''.join(content).replace(" ","").replace("\t","").replace("\n","")
        msgs = msg.split('。')[0:3]
        ms = "".join(msgs)
        print(ms)
        xw_toExcel(ms, ID)
    except Exception as FileNotFound:
        message = "File NotFound Error~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(message)
        with open("FileNotFound.txt", "a+", encoding="utf-8") as f:
            f.write(file_path)
            f.write("\n")


def Ocr_Ident(file_path, scene, ID):
    content = api_call(file_path, scene)
    data = content['data']['json']['general_ocr_res']['texts']
    msg = ""
    for da in data:
        msg += da
    msgs = msg.split('。')[0:3]
    ms = "".join(msgs)
    print(ms)
    xw_toExcel(ms, ID)


def Filereader_Ident(file_reader_engine, file_path, ID):
    filereader = FILEREADER(file_reader_engine, r"%s" % file_path)
    try:
        filereader.f_upload()
        filereader.f_inquire()
        msg = filereader.f_download()
        content = "".join(msg).replace('\n','')
        contents = content.split('。')[0:3]
        co = "".join(contents)
        print(co)
        xw_toExcel(co, ID)
    except Exception as FileNotFound:
        message = "File NotFound Error~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(message)
        with open("FileNotFound.txt", "a+", encoding="utf-8") as f:
            f.write(file_path)
            f.write("\n")



def SqlPath():
    num = 0
    for pa in SqlFiles():
        path = '/root/GuoDianTou' + pa[1] + pa[2]
        num += 1
        print(num,path)
        if os.path.splitext(path)[-1] in [".pdf", ".PDF"]:
            Filereader_Ident(file_reader_engine, path, pa[0])
        elif os.path.splitext(path)[-1] in ['.png', '.jpg', '.jpeg']:
            Ocr_Ident(path, scene, pa[0])
        elif os.path.splitext(path)[-1] == '.txt':
            Identification(path, pa[0])
        elif os.path.splitext(path)[-1] == '.docx':
            Docx_Ident(path, pa[0])
        elif os.path.splitext(path)[-1] == '.doc':
            Doc_Ident(path, pa[0])
        else:
            message = 'File suffix error'
            print(message)


SqlPath()
