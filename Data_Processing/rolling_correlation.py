'''
时间序列分析
输入：fund_clean.csv（清洗后的数据）
输出：滚动相关性矩阵图
作者：韩林利
依赖：pandas，numpy，matplotlib，senborn
最后更新时间：2025/3/5
'''
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ========== 第一步：数据加载与预处理 ==========
# 读取数据并转换日期格式
df = pd.read_csv('fund_clean.csv')  # 替换为实际文件路径
df['date'] = pd.to_datetime(df['date'])

# 关键处理1：确保每个基金每日唯一值
# 按基金和日期分组，取最后一条记录（假设数据已按日期排序）
clean_df = df.groupby(['ts_code', 'date']).last().reset_index()

# ========== 第二步：转换为宽表 ==========
# 使用adj_nav作为净值指标
pivot_df = clean_df.pivot(index='date', columns='ts_code', values='adj_nav')

# 关键处理2：前向填充缺失值（处理不同基金交易日不一致问题）
filled_df = pivot_df.ffill().dropna(how='all')

# ========== 第三步：计算月度收益率 ==========
# 重采样为月度数据（取每月最后一个有效值）
monthly_df = filled_df.resample('ME').last()

# 计算收益率并剔除首月（无变化值）
returns = monthly_df.pct_change().dropna()

# ========== 第四步：滚动相关性计算 ==========
def safe_rolling_corr(data, window=6):
    """带异常处理的滚动相关性计算"""
    # 设置最小有效期数为2（至少需要两个数据点计算相关性）
    return data.rolling(window=window, min_periods=2).corr(pairwise=True)

# 执行滚动计算（窗口改为6个月更适应示例数据时间范围）
rolling_corr = safe_rolling_corr(returns)
# 关键处理3：填充剩余NaN（用前值填充）
final_corr = rolling_corr.groupby(level=1).ffill()
print(final_corr)
# ========== 第五步：可视化 ==========
# 取最近时点的相关性矩阵
latest_date = final_corr.index.get_level_values(1).max()
latest_matrix = final_corr.xs(latest_date, level=1)

plt.figure(figsize=(15, 10))
sns.heatmap(
    latest_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    mask=np.triu(np.ones_like(latest_matrix)),
    annot_kws={"size": 8}
)

plt.title(f"滚动6个月基金收益率相关性矩阵（截至{latest_date.strftime('%Y-%m')}）")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('correct_rolling_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

print("相关性矩阵已保存为 correct_rolling_correlation.png")

# ========== 数据验证 ==========
print("\n数据质量检查：")
print("1. 月度收益率数据示例：")
print(returns.tail(3))
print("\n2. 相关性矩阵非空值比例：{:.1%}".format(latest_matrix.notnull().mean().mean()))



