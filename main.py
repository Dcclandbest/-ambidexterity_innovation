"""
-------------------------------------------------
   File Name：     main.py
   Description :   通过CSMAR生成双元创新数据
   Author :        Dcclandbest
   date：          2023.03.19
-------------------------------------------------
   Change Activity:
                   
-------------------------------------------------
"""

import os 
import pandas as pd

def clean_data(data,flag):
    drop_list = []
    for i,group_id in data.groupby('证券代码'):
        group_id.sort_values('year',inplace=True)
        group_year = group_id.groupby('year')
        temp = sorted(list(group_year.groups.keys()))
        if (len(group_year)!= temp[-1]-temp[0]+1) or (temp[-1]-temp[0]+1<= flag):
            try:
                data.drop(group_id.index,inplace=True)
            except KeyError as e:
                for _ in group_id.index:
                    data.drop(int(str(_).strip()),inplace=True)   
            drop_list.append(i)
    print('删除了 %s 个股票代码' %len(drop_list))  
    return data

def get_ipc(s):
    res = []
    for i in s:
        for j in str(i).strip().split(';'):
            if j!='':
                res.append(j.replace(' ','')[:4])
    return(list(set(res)))

def get_inn(data,flag):
    res = []
    for i,group_id in data.groupby('证券代码'):
        group_id.sort_values('year',inplace=True)
        group_year = group_id.groupby('year')
        temp = sorted(list(group_year.groups.keys()))

        for j in temp[flag:]:
            use_data={}
            use_data['year'] = j
            use_data['id'] = i 
            old_ipc=[]
            for _ in range(1,flag+1):
                old_ipc.extend(get_ipc(group_year.get_group(j-_)['分类号']))
            old_ipc = list(set(old_ipc))
            
            use_data['exploratory_inn'] = 0
            use_data['exploitative_inn'] = 0
            for patent in group_year.get_group(j)['分类号']:
                is_explore = 0
                for one_ipc in str(patent).strip().split(';'):
                    if one_ipc[:4] in old_ipc:
                        is_explore = 1
                if is_explore == 0:
                    use_data['exploratory_inn'] = use_data['exploratory_inn'] + 1
                if is_explore ==1:
                    use_data['exploitative_inn'] = use_data['exploitative_inn'] + 1
            res.append(use_data)
    return res

if __name__=="__main__":
    #区间设置
    FLAG = 3
    print(f"开始运行，区间长度为{FLAG}")

    # 第一步导入数据
    data = pd.read_excel('./PCT_Cited.xlsx')
    data_0 = pd.read_excel('./PCT_Cited2.xlsx')

    # # 由于数据量过大，所以需要拼接一下；对于拼接后的数据删除重复项
    data = pd.concat([data,data_0],axis=0)
    print("未删除重复项之前"+str(len(data.index)))
    data.drop_duplicates(['证券代码','申请号'],keep='first',inplace=True)
    print("删除重复项之后"+str(len(data.index)))

    # 根据申请号生成年份
    data['year'] = data['申请号'].apply(lambda x: int(x[0:4]))
    
    # 整理数据
    data.reset_index(drop=True,inplace=True)
    data.sort_values(['year','会计年度'],inplace=True)
    
    # 有些公司的数据不是连续的，有些公司数据连续长度小于区间阈值，对于这些数据进行删除
    data_cleaned = clean_data(data,FLAG)
    print("删除不符合长度的数据之后"+str(len(data_cleaned.index)))

    # 计算创新值
    res = get_inn(data_cleaned,FLAG)

    # 导出
    pd.DataFrame(res).to_excel('res_inn.xlsx')