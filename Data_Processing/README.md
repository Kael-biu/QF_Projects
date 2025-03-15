# 基金数据分析与风险评估

## 项目概述
本项目是一个完整的基金数据分析与风险评估流程，涵盖数据获取、清洗、优化、风险指标计算及相关性分析。通过Python脚本实现从原始数据到可视化结果的全流程自动化处理，适用于股票型基金的量化分析。

## 技术栈
- **编程语言**：Python
- **主要库**：
  - pandas：数据处理与分析
  - numpy：数值计算
  - tushare：金融数据获取
  - matplotlib/seaborn：数据可视化
  - openpyxl：Excel文件操作
- **工具**：Jupyter Notebook（可选）、GitHub

## 功能模块
1. **数据获取** (`fund_clean.py`)
   - 通过Tushare API获取股票型基金列表及近三年日线数据
   - 支持自定义筛选条件（如基金类型、时间范围）

2. **数据清洗** (`fund_clean.py` & `fund_clean_optimized.py`)
   - 缺失值处理：向前填充（FFill）
   - 异常值剔除：基于3σ原则的统计方法
   - 性能优化：使用pandas管道操作提升处理效率（优化后速度提升约30%）

3. **风险指标计算** (`fund_risk_indicators.py`)
   - 计算指标：
     - 年化波动率（Annual Volatility）
     - 最大回撤（Max Drawdown）
     - Calmar比率（年化收益/最大回撤绝对值）
   - 结果输出：生成包含原始数据与指标的Excel文件

4. **相关性分析** (`rolling_correlation.py`)
   - 计算月度收益率滚动相关性矩阵（6个月窗口）
   - 生成可视化热图，展示基金间动态相关性
   - 数据验证：检查收益率计算与矩阵完整性

5.**交互式报告**(`risk_calculator.ipynb`)
   - 使用下拉菜单选择不同基金代码
   - 自动更新显示净值曲线和风险指标
  

## 数据流程
```mermaid
graph TD
    A[获取原始数据] --> B[数据清洗]
    B --> C[计算风险指标]
    B --> D[转换为宽表]
    D --> E[计算滚动相关性]
    E --> F[可视化输出]
    F --> G[交互式面板]
**依赖项
%%pip install pandas numpy tushare matplotlib seaborn openpyxl
交互式数据面板 环境要求：jupyterlab ipywidgets matplotlib (需在 Jupyter Notebook中运行)
##使用说明
1.获取 Tushare API Token
  注册 Tushare 账号并获取 API Token，替换代码中的Your_token
2.运行数据清洗
  python fund_clean.py
  #或使用优化版本
  python fund_clean_optimized.py
3.计算风险指标
  python fund_risk_indicators.py
4.生成相关性矩阵
  python rolling_correlation.py
5.数据看板搭建(交互式面板)
  打开 risk_calculator.ipynb 文件并在 Jupyter Notebook 中运行

**优化说明
管道操作：将数据清洗步骤重构为 pandas 管道，代码可读性提升 33.41%
性能对比：
原始方法耗时：0.00599766秒
优化方法耗时：0.00399399秒（根据实际测试结果填写）
**输出结果
fund_clean.csv：清洗后的基金净值数据
fund_risk_indicators.xlsx：包含原始数据与风险指标的 Excel 文件
correct_rolling_correlation.png：基金收益率相关性热图
risk_calculator.ipynb：数据交互式面板

