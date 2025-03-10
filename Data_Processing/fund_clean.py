import tushare as ts
import pandas as pd

pro=ts.pro_api('Your_token')

#获取股票型基金列表
def get_stock_fund():
    #查询公募基金列表
    df=pro.fund_basic(market='E',status='L')
    #筛选股票型基金
    stock_fund=df[df['fund_type'].str.contains("股票型")].head(10)  #取前10支
    print('选中的股票型基金')
    print(stock_fund[['ts_code','name','fund_type']])
    return stock_fund['ts_code'].tolist()

#获取基金净值数据
def fetch_fund_data(fund_list):
    all_data=[]

    for ts_code in fund_list:
        #获取近三年的日线数据：
        df=pro.fund_nav(ts_code=ts_code,
                          start_date='20220201',
                          end_date='20250201')

        #标准化字段名称
        df=df.rename(columns={
            'nav_date':'date',
            'unit_nav':'net_value'
        })
        df['ts_code']=ts_code
        all_data.append(df)

    #合并所有基金数据
    full_df=pd.concat(all_data)
    #转换日期格式
    full_df['date']=pd.to_datetime(full_df['date'])
    return full_df.sort_values(['ts_code','date'])

#数据清洗
def clean_data(raw_df):
    #缺失值处理
    cleaned=raw_df.groupby('ts_code',group_keys=False).apply(lambda x: x.ffill().reset_index(drop=True))
    #3G剔除规则
    def remove_outliers(group):
        mean=group['net_value'].mean()
        std=group['net_value'].std()
        filtered=group[(group['net_value']>mean-3*std) &
                     (group['net_value']<mean+3*std)]
        return filtered.reset_index(drop=True)  #重置索引

    cleaned=cleaned.groupby('ts_code',group_keys=False).apply(remove_outliers)

    #重置索引
    return cleaned.reset_index(drop=False)



if __name__=='__main__':
    #获取基金列表：
    fund_codes=get_stock_fund()

    #获取原始数据
    raw_data=fetch_fund_data(fund_codes)
    print(f'\n原始数据实例：\n{raw_data.head()}')

    #清洗数据
    cleaned_data=clean_data(raw_data)

    #保存数据结果
    cleaned_data.to_csv('fund_clean.csv',index=True)
    print('\n清洗后数据已保存为 fund_clean.csv')

    #验证输出
    print('\n清洗后数据统计：')
    print(cleaned_data.groupby('ts_code').size())
    print('\n缺失值数量：')
    print(cleaned_data.isnull().sum())


