# -*- coding: utf-8 -*-
# -*- 弱小和无知不是生存的障碍，傲慢才是! -*-
# @author  : Fighter.Ma
# @Email   : fighter_ma1024@163.com
# @file    : b.py
# @time    : 2022/2/2422:56
# @Software: PyCharm

import pandas as pd

content = ['T', 'F'] * 10

data = pd.DataFrame(content, columns=['Y'])
print(data)

data.loc[data['Y'] == 'T'] = 1
data.loc[data['Y'] == 'F'] = 0

print(data)