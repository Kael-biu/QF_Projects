'''
性能优化
目标：将数据清洗过程改写为pandas管道操作，提升效率
'''
import pandas as pd
import numpy as np
import tushare as ts
from fund_clean import get_stock_fund
from fund_clean import fetch_fund_data
from fund_clean import clean_data
import time
#定义管道函数
def pipeline_ffill(df):
    '''向前填充管道函数'''
    return df.ffill()

def pipeline_remove_outliers(df):
    '''3α异常剔除管道函数'''
    mean=df['net_value'].mean()
    std=df['net_value'].std()
    return df[(df['net_value']>mean-3*std)&(df['net_value']<mean+3*std)]

def pipeline_optimize(group):
    '''分组管道操作'''
    return (
        group
        .pipe(pipeline_ffill)
        .pipe(pipeline_remove_outliers)
        .reset_index(drop=True)
    )

#主程序优化
def clean_data_pipeline(raw_df):
    '''管道化清洗主函数'''
    return (
        raw_df
        .groupby('ts_code',group_keys=False)
        .apply(pipeline_optimize)
        .reset_index(drop=True)
    )

#性能对比测试
if __name__=='__main__':
    #获取原始数据
    pro=ts.pro_api('Your_token')
    fund_codes = get_stock_fund()
    raw_data = fetch_fund_data(fund_codes)

    #原始方法计时
    start_time1=time.time()
    clean_data(raw_data)
    end_time1=time.time()
    times_1=end_time1-start_time1
    print("原始方法耗时：{:.5f}秒".format(times_1))

    #管道方法计时
    start_time2 = time.time()
    clean_data_pipeline(raw_data)
    end_time2= time.time()
    times_2 = end_time2 - start_time2
    print("管道方法耗时：{:.5f}秒".format(times_2))

    #保存优化后的数据
    optimized_data=clean_data_pipeline(raw_data)
    optimized_data.to_csv('fund_clean_optimized.csv',index=False)












