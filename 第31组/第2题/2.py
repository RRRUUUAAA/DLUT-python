import requests

from bs4 import BeautifulSoup

import pandas as pd
from pyecharts.charts import Line
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def crawl_weather_data():
    url = "https://www.tianqihoubao.com/lishi/dalian.html"
    res = requests.get(url)
    links = []


    for year in [2022, 2023, 2024]:
        for month in range(1, 13):
            links.append(f"https://www.tianqihoubao.com/lishi/dalian/month/{year}{month:02d}.html")
    all_data = []
    for url in links:
        try:
            resp = requests.get(url)
            lsoup = BeautifulSoup(resp.text, 'html.parser')
            table = lsoup.find('table')
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) < 4 or any('colspan' in str(col) for col in cols):
                    continue
                date = cols[0].get_text(strip=True)
                weather = cols[1].get_text(strip=True)
                temps = cols[2].get_text(strip=True)
                winds = cols[3].get_text(strip=True)
                all_data.append({"日期": date,
                              "天气（白天/夜间）": weather,
                             "气温（最高/最低）": temps,
                             "风力风向（白天/夜间）": winds})

        except Exception as e:
            print(f"错误{url}:{str(e)}")

    return all_data


weather_df = crawl_weather_data()
#括号二
from pyecharts.charts import Line
High_t = [0.0]*12
Low_t = [0.0]*12
for month in range(1,13):

    for days in weather_df:

        if days['日期'][5:7] == f'{month:02d}':

            s = days['气温（最高/最低）'].replace('℃','')
            l = s.split('/')
            High_t[month - 1] = round((High_t[month - 1]+int(l[0]))/2,2)
            Low_t[month - 1] = round((Low_t[month - 1]+int(l[1]))/2,2)

line = Line()
line.add_xaxis(range(1,13))
line.add_yaxis(series_name="平均最高气温",y_axis=High_t)
line.add_yaxis(series_name="平均最低气温",y_axis=Low_t)
line.render("月平均气温.html")

#括号三
from pyecharts.charts import Bar,Timeline
timeline = Timeline()

for month in range(1,13):
    count = [0] * 3  ##3-4||4-5||5-6
    for days in weather_df:

        if days['日期'][5:7] == f'{month:02d}':
            l = days['风力风向（白天/夜间）'].split('/')
            if '3-4' in l[0] or '3-4' in l[1]:
                count[0]= count[0] +1
            elif '4-5'in l[0] or '4-5' in l[1]:
                count[1]= count[1] +1
            elif '5-6'in l[0] or '5-6' in l[1]:
                count[2] = count[2]+1

    for x in range(3):
        count[x] = round(count[x]/3,2)

    bar = Bar()
    bar.add_xaxis(['3-4','4-5','5-6'])
    bar.add_yaxis(f"{month}月平均出现次数",count)
    timeline.add(bar,f'{month:02d}月')


timeline.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)

timeline.render("近三年平均每月风力.html")

#括号四

timeline = Timeline()

for month in range(1,13):
    count = {}  ##晴天、多云、阴天、雨天,雪等
    for days in weather_df:

        if days['日期'][5:7] == f'{month:02d}':
            l = days['天气（白天/夜间）'].replace(" ","").split('/')

            try:
               count[l[0]] = count[l[0]] +1
            except:
                count[l[0]] = 1
            try:
               count[l[1]] = count[l[1]] +1
            except:
                count[l[1]] = 1
    x:[str] =[]
    y=[]
    for k in count.keys():
        count[k] = round(count[k]/3,2)
        x.append(str(k))
        y.append(count[k])
    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis(f"{month}月平均出现次数",y)
    timeline.add(bar,f'{month:02d}月')


timeline.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)

timeline.render("近三年平均每月天气情况.html")

#括号五
from pyecharts.options import *
def crawl_2025_weather_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    links = []
    for month in range(1, 7):  # 2025年1-6月
        links.append(f"https://www.tianqihoubao.com/lishi/dalian/month/2025{month:02d}.html")

    all_data = []
    for url in links:
        try:
            resp = requests.get(url, headers=headers)#模拟请求头访问
            lsoup = BeautifulSoup(resp.text, 'html.parser')#指定使用python内置的解释器
            table = lsoup.find('table')
            for row in table.find_all('tr')[1:]:#跳过表头，寻找所有tr数据
                cols = row.find_all('td')
                if len(cols) < 4 or any('colspan' in str(col) for col in cols):#单元格数量小于4或者有合并单元格的情况
                    continue
                date = cols[0].get_text(strip=True)#去除文本空白字符
                weather = cols[1].get_text(strip=True)
                temps = cols[2].get_text(strip=True)
                winds = cols[3].get_text(strip=True)
                all_data.append({#将提取的值以字典的形式添加到all_data里
                    "日期": date,
                    "天气（白天/夜间）": weather,
                    "气温（最高/最低）": temps,
                    "风力风向（白天/夜间）": winds
                })
        except Exception as e:
            print(f"错误 {url}: {str(e)}")

    return all_data

def process_data(weather_data):
    monthly_high = [0.0] * 12  # 存储最高气温
    monthly_count = [0] * 12  # 存储月份

    for day in weather_data:
        try:
            date_str = day['日期']

            month = int(date_str.split('年')[1].split('月')[0])  # 不减1
            if month < 1 or month > 12:
                print(f"无效月份: {month}")
                continue
            month -= 1  # 转换为0-11

            temp_str = day['气温（最高/最低）'].replace('℃', '').strip()  # replace：去除摄氏度符号；strip：去除首尾空格
            if not temp_str:  # 当天为空字符串，则跳过
                continue

            temp_parts = temp_str.split('/')
            if len(temp_parts) < 2:
                print(f"温度数据格式错误: {temp_str}，数据: {day}")
                continue

            high_temp_str = temp_parts[0].strip()  # 提取最高温
            if high_temp_str:  # 检查最高温是否为空
                high_temp = int(high_temp_str)
                monthly_high[month] += high_temp
                monthly_count[month] += 1  # 统计当前月有效日期的个数，

        except (ValueError) as e:
            #print(f"处理数据时出错1: {e}, 数据: {day}")
            continue

        except (KeyError) as e:
           # print(f"处理数据时出错2: {e}, 数据: {day}")
            continue

        except (IndexError) as e:
           # print(f"处理数据时出错3: {e}, 数据: {day}")
            continue

        # 计算月平均值，处理可能除零的情况
    monthly_avg_high = [
        round(monthly_high[i] / monthly_count[i], 2) if monthly_count[i] > 0 else 0#round（...,2)将结果化为两位小数
        for i in range(12)
    ]

    return monthly_avg_high


# 爬取历史数据
historical_data = crawl_weather_data()
# 处理历史数据
historical_avg_high = process_data(historical_data)

# 爬取2025年1-6月真实数据
data_2025 = crawl_2025_weather_data()
# 处理2025年数据
actual_2025 = process_data(data_2025)[:6]  # 只取前6个月

# 训练预测模型 (使用多项式回归)
X = np.array(range(12)).reshape(-1, 1)  # 将（1-12）月转化为Numpy数组,scikit-learn需要二维数组,所以用reshape重塑为((12,1))二维
y = np.array(historical_avg_high)

# 使用3次多项式回归
model = make_pipeline(PolynomialFeatures(3), LinearRegression())#多项式回归+线性回归管道
model.fit(X, y)#训练

# 预测2025年各月份温度
X_pred = np.array(range(12)).reshape(-1, 1)
y_pred = model.predict(X_pred)#输出包含12个预测值的数组


# 只取前6个月的预测值
predicted_2025 = []
for x in y_pred[:6]:
    predicted_2025.append("%.2f"%x)
# 创建折线图
line = Line()#初始化折线图对象
line.add_xaxis([f"2025年{i + 1}月" for i in range(6)])
line.add_yaxis("实际平均最高温度", actual_2025, is_smooth=True)#是这项平滑连接而不是直线连接
line.add_yaxis("预测平均最高温度", predicted_2025, is_smooth=True)
line.set_global_opts(#设置全局选项
   # title_opts={"text": "大连市2025年1-6月实际与预测平均最高温度对比"},#标题
    yaxis_opts={"name": "温度(℃)"},#Y轴名称
    tooltip_opts={"trigger": "axis"}#设置提示框:鼠标悬停时，显示数据
)
line.set_global_opts(
    title_opts=TitleOpts(title="大连市2025年1-6月实际与预测平均最高温度对比",pos_left="center",pos_bottom="1%")
)
line.render("大连市2025年温度预测对比.html")

print("预测图表已生成: 大连市2025年温度预测对比.html")