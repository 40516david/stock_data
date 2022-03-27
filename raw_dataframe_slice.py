#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 14:57:56 2022

@author: huanghongru
"""
from datetime import datetime
import numpy as np
import pandas as pd
import os



def slice_dataframe(file_name):
    raw_path = '/Users/huanghongru/Desktop/股市歷史資料/Taiwan-Stock-Historical-Data/'
    csv_name = file_name + '.csv'
    
    df = pd.read_csv(raw_path + str(csv_name))    #讀取各股票csv檔案
    dfs = df['日期']
    date_list = dfs.tolist()
    
    
    new_list = []    #西元年列表
    
    #民國年轉西元年
    for dt in date_list:
    
        list_date = dt.split('/')
        
        year = int(list_date[0]) + 1911
        month = list_date[1]
        dt = str(year) + '-' + month + '-' + list_date[2]
        new_list.append(dt)
        
    #將df index轉為datetime
    df['西元年'] = pd.to_datetime(new_list)
    df.set_index('西元年',inplace = True)
    
    
    #跑出所有以年月份為單位資料的col
    list_col = []

    year = 2010
    month = 10
    
    for i in range(11) :
        while month < 13:
            if month < 10:
                datetime_col = str(year) + '-' + '0' + str(month)
            else:
                datetime_col = str(year) + '-' + str(month)
            list_col.append(datetime_col)
            month += 1
            #print(datetime_col)
        else:
            month = 1
        year += 1
    
    list_col = list_col[:-2]
    
    #依月分切割df並儲存成csv檔
    for dt in list_col:
        
        dfs = df[dt]
        dfs.reset_index(inplace = True)
        dfs = dfs.reset_index()
        
        #丟掉不要的col
        dfs = dfs.drop(['Unnamed: 0'],axis = 1)
        dfs = dfs.drop(columns = ['西元年'])
        dfs = dfs.drop(columns = ['index'])
        #print(dfs)
    
        path = '/Users/huanghongru/Desktop/crawler/stock_price/' + str(file_name) +'/'
        
        
        #save_file_name = str(file_name) + '-' + str(year) + '-' + str(month) + '.csv'   
        save_file_name = str(file_name) + '-' + dt + '.csv' #檔案命名規則
        if not os.path.isfile(path + save_file_name):
            dfs.to_csv(path + save_file_name)
            
            
path = '/Users/huanghongru/Desktop/crawler/stock_price/' 

allFileList = os.listdir(path)

for file_name in allFileList:
    try:
        slice_dataframe(file_name)
        print(file_name)
    except:
        print(file_name, 'Error')