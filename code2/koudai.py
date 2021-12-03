# 1.导入pandas模块
import pandas as pd
import os
import re
import numpy as np
from datetime import datetime
from pandas import DataFrame

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 50)


def getBanKuai():
    # 2.把Excel文件中的数据读入pandas
    bankuaiPath = '/Users/miketam/PycharmProjects/koudai/data/板块与股票表.xlsx'
    sheet = pd.read_excel(bankuaiPath, header=None, index_col=None, sheet_name=[0, 1, 2, 3])

    # 把几个表拼接
    df = sheet[0].append(sheet[1])
    df = df.append(sheet[2])
    df.columns = ['板块id', '板块名', '股票id', '股票名']

    # 把非"基金+北向持股"都股票去掉，
    df2 = sheet[3] # 基金北向持股列表在表3
    df2.columns = ['板块id2', '板块名2', '股票id', '股票名2']
    df2['key'] = 1
    df3 = pd.merge(df, df2, on='股票id', how="left")
    df3 = df3.drop(df3[np.isnan(df3['key']) == True].index).reset_index()
    df3 = df3.reset_index()
    return df3


# 统计某天的板块支点数
def getOneDayZd(dfBk, path, fileName):
    # 打开当天支点记录表
    print(fileName)
    dfZd = pd.read_csv(path + fileName, header=1, encoding="gbk", sep='\t')
    # 遗留：需要用正则提取股票id，目前用股票名来关联
    dfZd.rename(columns={'代码   ': '股票id', '名称': '股票名'}, inplace=True)  # 修改列索引
    dfZd = dfZd.loc[dfZd['AA1'] == 2, ['股票名', 'AA1', '股票id']]
    # 合并板块表与支点表
    df3 = pd.merge(dfBk, dfZd, on='股票名', how="left")
    dString = re.findall(r"\d+", fileName)  # 提取文件名中连续数字，这里是日期
    dFormat = datetime.strptime(dString[0], '%Y%m%d')

    # 分组和计算
    group = df3.groupby('板块名')
    # print(group.size())
    df4 = group.count().reset_index()[['板块名', '股票名', 'AA1']]  # 这里的"股票名" 实际是板块的股票数
    df4.rename(columns={'股票名': '股票数', 'AA1': '支点数'}, inplace=True)  # 修改列索引
    # 插入时间列
    df4.insert(0, '日期', value=dFormat)
    df4.insert(4, '支点比例', value=df4['支点数'] / df4['股票数'])
    # 增加支点数排序、支点比例排序两列
    df4.insert(5, '支点数排序', value=df4['支点数'].rank(method='first', ascending=False))
    df4.insert(6, '支点比例排序', value=df4['支点比例'].rank(method='first', ascending=False))
    # temp = df4.sort_values("支点比例排序", ascending=False, inplace=False)
    # print(temp)
    # # print(df4)
    # exit()
    return df4


# 获取板块与股票关系表
dfBanKuai = getBanKuai()

# 获取多天的板块支点数
zdPath = '/Users/miketam/PycharmProjects/koudai/data/口袋支点/'
files = os.listdir(zdPath)  # 所有文件名
dfAppend: DataFrame = pd.DataFrame()
for i in range(len(files)):
    # 打开1个文件口袋支点excel,
    # print(i)
    if '临时' in files[i]:  # 规避访问隐藏文件
        df = getOneDayZd(dfBanKuai, zdPath, files[i])
        dfAppend = dfAppend.append(df)
urlXlsx = '/Users/miketam/Downloads/test111.xlsx'
dfAppend.to_excel(urlXlsx, float_format='%.5f', index=False)
# print(dfAppend)
