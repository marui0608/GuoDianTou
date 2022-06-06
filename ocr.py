# # 弱小和无知不是生存的障碍，傲慢才是!
# coding=utf-8
import base64
import requests

server = "http://117.161.12.146:8513"


'''
    调用接口
    return: 返回json数据
'''
def api_call(image, scene):
    url = f'{server}/lab/ocr/predict/general'
    b64 = base64.b64encode(open(image, 'rb').read()).decode()
    data = {'scene': scene, 'image': b64,
            'parameters': {'vis_flag': False, 'sdk': True}}
    res = requests.post(url, json=data).json()
    return res


if __name__ == '__main__':

    image = r"D:\LabelTool\模型库\合同\data\Images\c15d9bf9f66f93e28f5c8ea20f90165.jpg"
    scene = "chinese_print"
    api_call(image=image, scene=scene)