# 1.导入pandas模块
import pandas as pd
import os
import re
import time
import numpy as np
from datetime import datetime
from pandas import DataFrame


# 显示所有列
# pd.set_option('display.max_columns', None)
# # 显示所有行
# pd.set_option('display.max_rows', None)
# # 设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth', 50)


pd.set_option('display.width',250)
pd.set_option('display.max_columns',130)
pd.set_option('display.max_colwidth',130)
pd.set_option('display.max_rows', None)


def getBanKuai():
    # 2.把Excel文件中的数据读入pandas
    bankuaiPath = '/Users/miketam/PycharmProjects/koudai/data/板块与股票表.xlsx'
    sheet = pd.read_excel(bankuaiPath, header=None, index_col=None, sheet_name=[0, 1, 2, 3])
    sheet[0]['type'] = '概念'
    sheet[1]['type'] = '行业'
    sheet[1][1] = sheet[1][1] + 'h'
    sheet[2]['type'] = '自定义'

    # 把几个表拼接
    df = sheet[0].append(sheet[1])
    df = df.append(sheet[2])
    df.columns = ['板块id', '板块名', '股票id', '股票名', '板块类型']


    df['板块id'] = df['板块id'].fillna(0)
    df['板块id'] = df['板块id'].apply(int)

    # 把非"基金+北向持股"都股票去掉，
    df2 = sheet[3]  # 基金北向持股列表在表3
    df2.columns = ['板块id2', '板块名2', '股票id', '股票名2']
    df2['key'] = 1
    df3 = pd.merge(df, df2, on='股票id', how="left")
    df3 = df3.drop(df3[np.isnan(df3['key']) == True].index).reset_index()
    df3 = df3.reset_index()
    # print(df3)
    # exit()

    return df3
    # return df


# 统计某天的板块支点数
def getOneDayZd(dfBk, path, fileName):
    # 打开当天支点记录表
    print(fileName)
    dfZd = pd.read_csv(path + fileName, header=1, encoding="gbk", sep='\t')
    # 遗留：需要用正则提取股票id，目前用股票名来关联
    dfZd.rename(columns={'代码   ': '股票id', '名称': '股票名'}, inplace=True)  # 修改列索引
    dfZd = dfZd.loc[dfZd['AA1'] == 2, ['股票名', 'AA1', '股票id']] # 只保留是支点的行
    dfZd = dfZd.reset_index()

    # 合并板块表与支点表；
    # 遗留问题：随着时间推移，基金+北向的股池会变化越来越大，原来的支点记录数据会与股池对不上，那么历史板块支点走势可能出现不够准确
    df3 = pd.merge(dfBk, dfZd, on='股票名', how="left")  # 板块表是承载板块与股票的关系
    df3 = df3[['板块id', '板块名', '板块类型', '股票名', 'AA1']]

    dString = re.findall(r"\d+", fileName)  # 提取文件名中连续数字，这里是日期
    dFormat = datetime.strptime(dString[0], '%Y%m%d')

    # 分组和计算， 计算板块股票数量、计算板块支点数量
    group = df3[['板块名', '股票名', 'AA1']].groupby('板块名')  #
    df4 = group.count().reset_index()[['板块名', '股票名', 'AA1']]  # 这里的"股票名" 实际是板块的股票数
    df4.rename(columns={'股票名': '股票数', 'AA1': '支点数'}, inplace=True)  # 修改列索引
    df5 = df3.drop_duplicates(subset=['板块名'], keep='last')  # 取板块类型值
    df4 = pd.merge(df4, df5[['板块名', '板块类型', '板块id']], on='板块名', how="left")
    df4['相关板块'] = 'text'

    # 统计有支点板块与相关板块的数据: 共有股票的板块排序和具体股票名
    # 程序逻辑:
    # 1)逐个找板块对应的支点股票，比如板块1有4个股票
    # 2）通过4个股票筛选出所有板块与股票记录
    # 3）根据板块名对这个记录分组，得到各板块都股数（这4各当中都股票）
    # 4）对这些板块进行排序放入
    df3 = df3.loc[df3['AA1'] == 2]  # 只保留有支点的记录
    group2 = df3.groupby('板块名')
    x = 0
    for a in group2:
        x = x + 1
        nameBk = a[0]
        dfOneBk = a[1]
        # 取取该板块的几个股票，然后再用这个几个股票提取所以相关板块，然后分组
        stocks = dfOneBk['股票名']

        dfTemp = df3.loc[df3['股票名'].isin(stocks)]
        dfTemp = dfTemp.groupby(['板块名'])["股票名"].apply(list).to_frame() # 分组并把"股票名"的行内容合并
        dfTemp = dfTemp.reset_index()

        # dfTemp['股票数'] = dfTemp['股票名'].map(len)
        dfTemp['股票数'] = dfTemp['股票名'].map(lambda x: len(x))  # map表示对该列操作，x就是那行值。 apply是表示对表操作
        dfTemp.insert(dfTemp.shape[1], '股票数排序', value=dfTemp['股票数'].rank(method='first', ascending=False))
        dfTemp = dfTemp.sort_values('股票数排序', ascending=True, inplace=False)
        dfTemp['股票数'] = dfTemp['股票数'].apply(str)
        dfTemp['股票数排序'] = dfTemp['股票数排序'].apply(str)
        # dfTemp['股票名'] = dfTemp['股票名'].apply('.'.join(list))
        dfTemp['股票名'] = dfTemp['股票名'].map(lambda x: ','.join(x))  # 把list该为str
        #合并列内容
        dfTemp['列合并'] = dfTemp['股票数排序'] + '[' + dfTemp['板块名'] + '-' + dfTemp['股票数'] + '-' + dfTemp['股票名'] + ']' + ', '
        dfTemp = dfTemp.reset_index()
        text = ''
        # 合并前10行组成相关板块文本, 如果少于10行就取已有的
        count = 10
        if dfTemp.shape[0] < count:
            count = dfTemp.shape[0]
        for y in range(count):
            text = text + dfTemp.at[y, '列合并'] + '\n'  # 相关板块的文本内容
        df4.loc[df4['板块名'] == nameBk, '相关板块'] = text


    # 插入时间列

    df4.insert(df4.shape[1], '日期', value=dFormat)
    df4.insert(df4.shape[1], '支点比例', value=df4['支点数'] / df4['股票数'])
    # 增加支点数排序、支点比例排序两列
    df4.insert(df4.shape[1], '支点数排序', value=df4['支点数'].rank(method='first', ascending=False))
    df4.insert(df4.shape[1], '支点比例排序', value=df4['支点比例'].rank(method='first', ascending=False))
    # temp = df4.sort_values("支点比例排序", ascending=False, inplace=False)

    dfZd.insert(dfZd.shape[1], '日期', value=dFormat) #支点列表
    dfBkZd = df4  # 板块与支点数关联


    # print(df4)

    # dfBkZdBk # 板块与板块关联（有支点的板块的股票还在哪些板块，可能发现比当前板块更强的板块）
    # dfGgZdBk # 个股与板块关联 (有支点的个股与哪些板块关联）
    # dfBkGgList  # 板块与个股的对应关系，与日期、支点无关
    # dfGgBkList  # 个股与板块的对应关系，与日期、支点无关

    # print(df4)
    # exit()
    #
    # #  计算概念板块的支点股票所属的行情板块组成； 计算行业板块的支点股票所属的概念板块组成。
    # df6 = df3[df3['AA1'] == 2] # 提取所有支点
    # print(df6)
    # exit()
    return dfBkZd, dfZd


# 单独导出通达信要的数据
def tdxData(df):
    # 单独导出适用与通达信导入的板块支点数文件

    df['market'] = 1  # '上海市场'
    df.loc[df['板块类型'] == '自定义', 'market'] = 0
    # print(df)
    # exit()

    # df.insert(0, 'market', value=1)
    df['日期'] = df['日期'].dt.strftime('%Y%m%d')

    df['temp'] = '-'
    df4 = df.loc[df['日期'] == '20211115', ['market', '板块id', 'temp', '股票数']]  #随意取1日数据提取股票数
    urlXlsx = '/Users/miketam/Downloads/1-股票数.txt'
    df4.to_csv(urlXlsx, sep='|', index=False, header=False)

    df1 = df[['market', '板块id', '日期', '支点数']]
    urlXlsx = '/Users/miketam/Downloads/2-支点数.txt'
    df1.to_csv(urlXlsx, sep='|', index=False, header=False)

    df2 = df[['market', '板块id', '日期', '支点数排序']]
    urlXlsx = '/Users/miketam/Downloads/3-支点数排序.txt'
    df2.to_csv(urlXlsx, sep='|', index=False, header=False)

    df3 = df[['market', '板块id', '日期', '支点比例排序']]
    urlXlsx = '/Users/miketam/Downloads/4-支点比例排序.txt'
    df3.to_csv(urlXlsx, sep='|', index=False, header=False)
    return


#  获取板块与股票关系表
dfBanKuai = getBanKuai()

# 获取多天的板块支点数
zdPath = '/Users/miketam/PycharmProjects/koudai/data/口袋支点/'
files = os.listdir(zdPath)  # 所有文件名
dfAppend: DataFrame = pd.DataFrame()
dfAppend2: DataFrame = pd.DataFrame()

tis1 = time.perf_counter()
for i in range(len(files)):
    # 打开1个文件口袋支点excel,
    # print(i)
    if '临时' in files[i]:  # 规避访问隐藏文件
        temp = getOneDayZd(dfBanKuai, zdPath, files[i])
        dfBkZd = temp[0]
        dfZd = temp[1]
        dfAppend = dfAppend.append(dfBkZd)
        dfAppend2 = dfAppend2.append(dfZd)
    # if i > 1:
    #     break
tis2 = time.perf_counter()
print("处理时间：")
print(tis2 - tis1)
# 有时在这测试代码，计算运行时间#
dfAppend = dfAppend.sort_values(by='日期')
dfAppend2 = dfAppend2.sort_values(by='日期')

dftemp2 = dfAppend.copy(deep=True)
tdxData(dftemp2)  # 处理通达信导出


urlXlsx = '/Users/miketam/Downloads/test112.xlsx'
# dfAppend.to_excel(urlXlsx, float_format='%.5f', index=False)
with pd.ExcelWriter(urlXlsx) as writer:  # 创建多个表
    dfAppend.to_excel(writer, sheet_name="sheet1")  # 表1：按日显示板块支点数
    dfAppend[['日期', '板块名', '支点数排序', '支点比例排序']].to_excel(writer, sheet_name="sheet2")  # 表2：单独显示支点排序
    dfAppend2.to_excel(writer, sheet_name='每天支点')  # 每天的有支点股票列表
    dfBanKuai[['板块名', '股票名', '板块类型']].to_excel(writer, sheet_name='板块与股票')  # 板块与股票对应关系







