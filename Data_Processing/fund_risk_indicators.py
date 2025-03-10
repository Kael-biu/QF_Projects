import pandas as pd
import numpy as np

#1.数据加载
cleaned_data=pd.read_csv('fund_clean.csv')
cleaned_data['date']=pd.to_datetime(cleaned_data['date'])
#2.定义指标计算函数
def calculate_metrics(group):
    #计算日收益率
    returns=group['net_value'].pct_change().dropna()

    #年化波动率
    annual_volatility=returns.std()*np.sqrt(252)

    #最大回撤
    cumulative_max=group['net_value'].cummax()
    drawdown=(group['net_value']-cumulative_max)/cumulative_max
    max_drawdown=drawdown.min()

    #年化收益率
    total_return=(group['net_value'].iloc[-1]/group['net_value'].iloc[0])-1
    annual_return=(1+total_return)**(252/len(group))-1

    #Calmar比率（年化收益/最大回撤，取绝对值）
    calamr_ratio=abs(annual_return/max_drawdown)if max_drawdown !=0 else np.nan

    return pd.Series({
        '年化波动率':annual_volatility,
        '最大回撤':max_drawdown,
        'Calamr比率':calamr_ratio
    })

#3.批量计算所有基金指标
#按基金分组计算
risk_indicators=cleaned_data.groupby('ts_code').apply(calculate_metrics)

#重置索引并重命名
risk_indicators=risk_indicators.reset_index().rename(columns={'level_1':'指标'})

#4.保存结果
with pd.ExcelWriter('fund_risk_indicators.xlsx',engine='openpyxl') as writer:
    cleaned_data.to_excel(writer,sheet_name='净值数据',index=False)
    risk_indicators.to_excel(writer,sheet_name='风险指标',index=False)

print('风险指标已保存在 fund_risk_indicators.xlsx')





