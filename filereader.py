# # 弱小和无知不是生存的障碍，傲慢才是!
# coding=utf-8
import os
import time
from requests import post, get


class FILEREADER:

    def __init__(self, engine, data):
        """
        engine: FileReader 服务端
        data: 待上传pdf
        """
        self.task_no = ''
        self.totalSub_task = ''
        self.processSub_task = ''
        self.doneSub_task = ''
        self.msgContent = ''
        self.main_fr, self.data = engine, data
        self.upload_fr = self.main_fr + 'readFileAsync'
        self.inquire_fr = self.main_fr + 'getResult'
        self.download_fr = self.main_fr + 'getResultFile'

    def f_upload(self):
        """PDF上传并赋值任务编号"""
        print(f'开始上传PDF文件\nf<{self.data}>\n请等待……')
        data = {'file': (os.path.split(self.data)[-1], open(self.data, 'rb'))}
        result_up = post(url=self.upload_fr, files=data).json()
        self.task_no = result_up['data'] if result_up['code'] == 200 else None
        print('PDF上传成功，任务编号：{}\n'.format(self.task_no))

    def f_inquire(self):
        """查询任务结果"""
        print('开始查询任务结果……')
        data = {'taskNo': self.task_no, 'totalSubTask': self.totalSub_task, 'processSubTask': self.processSub_task, 'doneSubTask': self.doneSub_task}
        num = 3
        while True:
            re = get(url=self.inquire_fr, params=data).json()
            # time.sleep(5)
            # print(re['data'])
            totalSubTask = re['data']['totalSubTask']
            processSubTask = re['data']['processSubTask']
            doneSubTask = re['data']['doneSubTask']
            if totalSubTask == 1 and processSubTask == 0 and doneSubTask == 0:
                print(num)
                if not num:
                    break
                num = num - 1
            state = re['data']['state']
            if state == 30:
                break
            time.sleep(2)


    def f_download(self):
        """下载对应实例"""
        print('开始获取实例内容……')
        data = {'name': self.task_no, 'fileType': 1}
        re = get(url=self.download_fr, params=data)
        print('获取内容完毕！\n')
        return re.text


if __name__ == '__main__':

    file_reader_engine = 'http://117.161.12.146:8516/service/'
    # data = r"C:\Users\Lenovo\Desktop\4paradigm部署\FileReader快速部署手册.pdf"
    # data = r"D:\Xshell7_en.pdf"
    data = r"C:\Users\Lenovo\Desktop\8ad0b0c26fb3b6e5016fcb48b7d74e9a_1775073b6e17809e8e947702516c11cf.pdf"
    f = FILEREADER(file_reader_engine, data)
    print('「------------------------------')
    # 1
    f.f_upload()
    # 2
    f.f_inquire()
    # # 3
    pdf_content = f.f_download()
    # print(pdf_content[:50])
    print(pdf_content)