import requests
import json
import pandas as pd
from pyecharts.charts import Line
import time
import random
from bs4 import BeautifulSoup
import re

from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

import ast


def crawl_DBLP_data():
    confs = ['aaai', 'ijcai', 'cvpr', 'iccv']
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    all_data = []
    for conf in confs:
        for year in years:
            url = f"https://dblp.org/db/conf/{conf}/{conf}{year}.html"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for entry in soup.find_all('li', class_='entry'):
                data = entry.find('cite', class_='data')
                title = data.find('span', class_='title').text.strip()
                authors = [a.text for a in data.find_all('span', itemprop='author')]
                ee_link = entry.find('li', class_='ee').find('a').get('href')
                all_data.append({"论文标题": title,
                                 "作者": authors,
                                 "发表年份": year,
                                 "会议名称": conf,
                                 "原始链接": ee_link})

    return all_data

#先运行保存成txt在电脑中，为后续调试节省时间
# DBLP_data = crawl_DBLP_data()
# f = open("D:/3.txt", "w", encoding="utf-8")
# f.write(str(DBLP_data))
# f.flush()
# f.close()
#
# with open("D:/3.txt","r",encoding="UTF-8") as f :
#     data = f.read()
# data_list = ast.literal_eval(data)
data_list = crawl_DBLP_data()


#统计一下各个会议都在哪些年份

# d :{str:list}= {}
# for n in data_list:
#     if n['会议名称'] not in d.keys():
#         d[n['会议名称']] = []
#         d[n['会议名称']].append(n['发表年份'])
#     else:
#         if n['发表年份'] in d[n['会议名称']]:
#             continue
#         d[n['会议名称']].append(n['发表年份'])
#print(d)
#运行结果：{'aaai': [2020, 2021, 2022, 2023, 2024, 2025],
#         'ijcai': [2020, 2021, 2022, 2023, 2024],
#         'cvpr': [2020, 2021, 2022, 2023, 2024],
#         'iccv': [2021, 2023]}

aaai_num = [0] * 6
ijcai_num = [0] * 6
cvpr_num = [0] * 6
iccv_num = [0] * 6
words_2020 ={}
words_2021 ={}
words_2022 ={}
words_2023 ={}
words_2024 ={}
words_2025 ={}
for n in data_list:
    if n['会议名称'] == 'aaai':
        if n['发表年份'] == 2020:
            aaai_num[0] += 1
        elif n['发表年份'] == 2021:
            aaai_num[1] += 1
        elif n['发表年份'] == 2022:
            aaai_num[2] += 1
        elif n['发表年份'] == 2023:
            aaai_num[3] += 1
        elif n['发表年份'] == 2024:
            aaai_num[4] += 1
        elif n['发表年份'] == 2025:
            aaai_num[5] += 1
    elif n['会议名称'] == 'ijcai':
        if n['发表年份'] == 2020:
            ijcai_num[0] += 1
        elif n['发表年份'] == 2021:
            ijcai_num[1] += 1
        elif n['发表年份'] == 2022:
            ijcai_num[2] += 1
        elif n['发表年份'] == 2023:
            ijcai_num[3] += 1
        elif n['发表年份'] == 2024:
            ijcai_num[4] += 1
        elif n['发表年份'] == 2025:
            ijcai_num[5] += 1
    if n['会议名称'] == 'cvpr':
        if n['发表年份'] == 2020:
            cvpr_num[0] += 1
        elif n['发表年份'] == 2021:
            cvpr_num[1] += 1
        elif n['发表年份'] == 2022:
            cvpr_num[2] += 1
        elif n['发表年份'] == 2023:
            cvpr_num[3] += 1
        elif n['发表年份'] == 2024:
            cvpr_num[4] += 1
        elif n['发表年份'] == 2025:
            cvpr_num[5] += 1
    if n['会议名称'] == 'iccv':
        if n['发表年份'] == 2020:
            iccv_num[0] += 1
        elif n['发表年份'] == 2021:
            iccv_num[1] += 1
        elif n['发表年份'] == 2022:
            iccv_num[2] += 1
        elif n['发表年份'] == 2023:
            iccv_num[3] += 1
        elif n['发表年份'] == 2024:
            iccv_num[4] += 1
        elif n['发表年份'] == 2025:
            iccv_num[5] += 1
    Title = n['论文标题'].replace(":"," ").replace(").","").split(" ")
    mean_less = ["for","For","of","On","with","to","To","the","a","A","an","and","Is",
                 "up","Up","&","as","are","Be","it","It","via","can","vs.","from","is",
                 "Can","at","by","By","As","I","do","One","Are","Me","we","Its","or","its",
                   "on","The","Yet","An","not" ,"All","What","in","your","You","From","Do"]
    if n['发表年份'] == 2020:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2020[word] += 1
            except:
                words_2020[word] = 1

    if n['发表年份'] == 2021:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2021[word] += 1
            except:
                words_2021[word] = 1

    if n['发表年份'] == 2022:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2022[word] += 1
            except:
                words_2022[word] = 1
    if n['发表年份'] == 2023:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2023[word] += 1
            except:
                words_2023[word] = 1
    if n['发表年份'] == 2024:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2024[word] += 1
            except:
                words_2024[word] = 1
    if n['发表年份'] == 2025:
        for word in Title:
            if word in mean_less:
                continue
            try:
                words_2025[word] += 1
            except:
                words_2025[word] = 1
#括号二
from pyecharts.charts import Line

line = Line()
line.add_xaxis(["2020","2021","2022","2023","2024","2025"])
line.add_yaxis(series_name="aaai",y_axis=aaai_num)
line.add_yaxis(series_name="ijcai",y_axis=ijcai_num)
line.add_yaxis(series_name="cvpr",y_axis=cvpr_num)
line.add_yaxis(series_name="iccv",y_axis=iccv_num)

line.render("各个会议2020年至今每届论文数量变化趋势图.html")


#["2020","2021","2022","2023","2024","2025"]
#[2020,2021,2022,2023,2024,2025]
#括号三
from pyecharts.charts import WordCloud,Timeline
timeline = Timeline()
word_cloud_2020 = WordCloud()
word_cloud_2020.add("", words_2020.items(), word_size_range=[12, 55])
word_cloud_2021 = WordCloud()
word_cloud_2021.add("", words_2021.items(), word_size_range=[12, 55])
word_cloud_2022 = WordCloud()
word_cloud_2022.add("", words_2022.items(), word_size_range=[12, 55])
word_cloud_2023 = WordCloud()
word_cloud_2023.add("", words_2023.items(), word_size_range=[12, 55])
word_cloud_2024 = WordCloud()
word_cloud_2024.add("", words_2024.items(), word_size_range=[12, 55])
word_cloud_2025 = WordCloud()
word_cloud_2025.add("", words_2025.items(), word_size_range=[12, 55])

timeline.add_schema(
    play_interval=10000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)

timeline.add(word_cloud_2020,"2020年")
timeline.add(word_cloud_2021,"2021年")
timeline.add(word_cloud_2022,"2022年")
timeline.add(word_cloud_2023,"2023年")
timeline.add(word_cloud_2024,"2024年")
timeline.add(word_cloud_2025,"2025年")
timeline.render("各年词云图.html")

# 括号四：论文数量预测，线性回归模型

# 设置中文字体和负号显示
rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 使用黑体或苹果字体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 准备各会议的历史数据
conferences = {
    'aaai': {'years': [], 'counts': []},
    'ijcai': {'years': [], 'counts': []},
    'cvpr': {'years': [], 'counts': []},
    'iccv': {'years': [], 'counts': []}
}

# 填充有效数据
for i, year in enumerate([2020, 2021, 2022, 2023, 2024, 2025]):
    if aaai_num[i] > 0:
        conferences['aaai']['years'].append(year)
        conferences['aaai']['counts'].append(aaai_num[i])
    if ijcai_num[i] > 0:
        conferences['ijcai']['years'].append(year)
        conferences['ijcai']['counts'].append(ijcai_num[i])
    if cvpr_num[i] > 0:
        conferences['cvpr']['years'].append(year)
        conferences['cvpr']['counts'].append(cvpr_num[i])
    if iccv_num[i] > 0:
        conferences['iccv']['years'].append(year)
        conferences['iccv']['counts'].append(iccv_num[i])

# 预测函数（预测2026年）
def predict_with_linear_regression(years, counts, conference_name):
    if len(years) < 2:
        print(f"{conference_name.upper()}: 数据不足（只有{len(years)}年数据），无法进行线性回归预测")
        return None

    # 准备数据
    X = np.array(years).reshape(-1, 1)
    y = np.array(counts)

    # 训练模型
    model = LinearRegression()
    model.fit(X, y)

    # 预测2026年
    predict_year = 2026
    prediction = model.predict([[predict_year]])[0]

    # 创建图表
    plt.figure(figsize=(10, 6), dpi=120)  # 提高分辨率和尺寸

    # 绘制实际数据点
    plt.scatter(X, y, color='#1f77b4', s=80, label='实际数据', zorder=3)

    # 绘制回归线和预测范围
    x_vals = np.linspace(min(years) - 1, 2026, 100).reshape(-1, 1)
    plt.plot(x_vals, model.predict(x_vals),
             color='#ff7f0e',
             linewidth=2.5,
             label='回归趋势线',
             zorder=2)

    # 标记预测点
    plt.scatter([predict_year], [prediction],
                color='#2ca02c',
                marker='*',
                s=300,
                label='2026年预测值: {}篇'.format(int(round(prediction))),
                zorder=4)

    # 添加数据标签
    for x, y_val in zip(years, counts):
        plt.text(x, y_val, f'{y_val}',
                 ha='center', va='bottom',
                 fontsize=9, color='#1f77b4')

    # 设置图表元素
    plt.title(f'{conference_name.upper()}会议论文数量趋势预测', fontsize=14, pad=20)
    plt.xlabel('年份', fontsize=12, labelpad=10)
    plt.ylabel('论文数量（篇）', fontsize=12, labelpad=10)

    # 设置坐标轴范围
    plt.xlim(min(years) - 1, 2026)
    plt.ylim(0, max(counts) * 1.2)

    # 设置刻度
    all_years = sorted(list(years) + [predict_year])
    plt.xticks(all_years, fontsize=10)
    plt.yticks(fontsize=10)

    # 网格和样式
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left', fontsize=10, framealpha=0.9)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(f'{conference_name}_2026年预测.png',
                bbox_inches='tight',
                dpi=150,
                facecolor='white')
    plt.close()

    return max(0, round(prediction))

# 对各会议进行2026年预测
predictions_2026 = {}
for conf, data in conferences.items():
    if len(data['years']) >= 2:  # 至少需要2个数据点才能做线性回归
        pred = predict_with_linear_regression(data['years'], data['counts'], conf)
        if pred is not None:
            predictions_2026[conf] = pred

# 打印预测结果
print("\n2026年各会议预测论文数量（基于线性回归）:")
for conf, pred in predictions_2026.items():
    print(f"{conf.upper()}: {pred}篇")

# 保存预测结果
pred_df = pd.DataFrame.from_dict(predictions_2026, orient='index', columns=['2026年预测数量'])
pred_df.to_csv('各会议2026年论文数量预测.csv', encoding='utf_8_sig')  # 确保CSV中文正常
print("\n预测结果已保存到 各会议2026年论文数量预测.csv")