import requests
import json
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
import re

from docutils.nodes import title


def crawl_lottery_data():
    headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
             "Referer": "https://www.zhcw.com/"}
    lottery_data = []
    for page in range(1,5):
        url=f'https://jc.zhcw.com/port/client_json.php?callback=jQuery1122022565455290666903_1752134012470&transactionType=10001001&lotteryId=281&issueCount=0&startIssue=0&endIssue=0&startDate=2024-10-01&endDate=2025-07-01&type=2&pageNum={page}&pageSize=30&tt=0.6607845790385086&_=1752134012480'
        res = requests.get(url,headers=headers)
        raw_data = res.text
        json_start = raw_data.find('{')
        json_end = raw_data.rfind('}') + 1
        json_str = raw_data[json_start:json_end]
        data_obj = json.loads(json_str)
        for item in data_obj["data"]:
            lottery_data.append({"期号":item["issue"],
                            	"开奖日期":item["openTime"],
                              	"前区号码":item["frontWinningNum"],
                              	"后区号码":item["backWinningNum"],
                              	"总销售额（元）":item["saleMoney"],
                             	"星期几":item["week"]})

    return lottery_data

def crawl_expert_data():
    headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
             "Referer": "https://www.zhcw.com/"}
    experts = ['2474215','1323597','2482176','1717763','2373361',
               '1857709','2475109','2960437','2157438','2914982',
               '2421927','1971542','3005226','1771952','3055732',
               '3036312','2998708','3038398','2372772','2491726']
    expert_data = []
    for expert in experts:
        url = f'https://i.cmzj.net/expert/queryExpertById?expertId={expert}'
        res = requests.get(url,headers=headers)
        raw_data = res.json()
        dltPrize = "一等奖:"+str(raw_data['data']['dltOne'])+" 二等奖:"+str(raw_data['data']['dltTwo'])+" 三等奖:"+str(raw_data['data']['dltThree'])
        ssqPrize =  "一等奖:"+str(raw_data['data']['ssqOne'])+" 二等奖:"+str(raw_data['data']['ssqTwo'])+" 三等奖:"+str(raw_data['data']['ssqThree'])
        expert_data.append({"专家名称":raw_data['data']['name'],
                         	"彩龄":raw_data['data']['age'],
    	                   "发文量":raw_data['data']['articles'],
                          	"关注数量":raw_data['data']['fans'],
                          	"大乐透中奖情况":dltPrize,
                          	"双色球中奖情况":ssqPrize})
    return expert_data

lottery_data = crawl_lottery_data()
expert_data = crawl_expert_data()
Date = []
E = []
F_num = {}
B_num = {}
F_Mon_num = {}#周一前区
B_Mon_num = {}#周一后区
F_Wed_num = {}#周三前区
B_Wed_num = {}#周三后区
F_Sat_num = {}#周六前区
B_Sat_num = {}#周六后区
Sum = [0]*3 #总销售额：周一、周三、周六
for x in lottery_data:
    Date.append(str(x['开奖日期']))
    E.append(str(x['总销售额（元）']))
    if x['星期几'] == '星期一':
        Sum[0] = (Sum[0]+int(x['总销售额（元）']))/2
    elif x['星期几'] == '星期三':
        Sum[1] = (Sum[1] + int(x['总销售额（元）'])) / 2
    else:
        Sum[2] = (Sum[2] + int(x['总销售额（元）'])) / 2
    for n in x['前区号码'].split(" "):
        try:
            F_num[n] +=  1
        except:
            F_num[n] = 1
        if x['星期几'] == '星期一':
            try:
                F_Mon_num[n] += 1
            except:
                F_Mon_num[n] = 1
        elif x['星期几'] == '星期三':
            try:
                F_Wed_num[n] += 1
            except:
                F_Wed_num[n] = 1
        else:
            try:
                F_Sat_num[n] += 1
            except:
                F_Sat_num[n] = 1
    for n in x['后区号码'].split(" "):
        try:
            B_num[n] +=  1
        except:
            B_num[n] = 1
        if x['星期几'] == '星期一':
            try:
                B_Mon_num[n] += 1
            except:
                B_Mon_num[n] = 1
        elif x['星期几'] == '星期三':
            try:
                B_Wed_num[n] += 1
            except:
                B_Wed_num[n] = 1
        else:
            try:
                B_Sat_num[n] += 1
            except:
                B_Sat_num[n] = 1


from pyecharts.charts import Line
from pyecharts.options import *
line = Line()
line.add_xaxis(Date)
line.add_yaxis("总销售额",E,label_opts=LabelOpts(is_show=False))
line.render("总销售额随开奖日期的变化.html")

#从已有数据中提取最近几期的销售额
recent_sales = [int(x['总销售额（元）']) for x in lottery_data[-5:]]  #取最近5期数据
avg_recent = sum(recent_sales) / len(recent_sales)

#获取周三和周六的历史平均销售额
wed_avg = Sum[1]  #周三平均销售额
sat_avg = Sum[2]  #周六平均销售额

#预测最近一期的销售额
next_date = "2025-07-02"
next_sale_prediction = (wed_avg + avg_recent) / 2  #综合历史平均和近期趋势

print(f"预测{next_date}最近一期的销售额约为: {int(next_sale_prediction):,}元")

#括号二
from pyecharts.charts import Bar
bar = Bar()
f_num_sorted = sorted(F_num.items(),key=lambda x:x[1],reverse=True)
b_num_sorted = sorted(B_num.items(),key=lambda x:x[1],reverse=True)
f_x = []
f_y = []

for n in f_num_sorted:
    f_x.append(n[0])
    f_y.append(n[1])

b_x = []
b_y = []
for n in b_num_sorted:
    b_x.append(n[0])
    b_y.append(n[1])
bar.add_xaxis(f_x)
bar.add_yaxis("出现频次",f_y)
bar.render("前区号码频率排名.html")

bar2 = Bar()
bar2.add_xaxis(b_x)
bar2.add_yaxis("出现频次",b_y)
bar2.render("后区号码频率排名.html")


def recommend_dlt_numbers():
    #获取每周各天前区出现频率最高的5个号码
    top_mon_front = sorted(F_Mon_num.items(), key=lambda x: x[1], reverse=True)[:5]
    top_wed_front = sorted(F_Wed_num.items(), key=lambda x: x[1], reverse=True)[:5]
    top_sat_front = sorted(F_Sat_num.items(), key=lambda x: x[1], reverse=True)[:5]

    #获取每周各天后区出现频率最高的2个号码
    top_mon_back = sorted(B_Mon_num.items(), key=lambda x: x[1], reverse=True)[:2]
    top_wed_back = sorted(B_Wed_num.items(), key=lambda x: x[1], reverse=True)[:2]
    top_sat_back = sorted(B_Sat_num.items(), key=lambda x: x[1], reverse=True)[:2]

    #合并所有高频号码
    frequent_front = top_mon_front + top_wed_front + top_sat_front
    frequent_back = top_mon_back + top_wed_back + top_sat_back

    #按加权频率选择
    #前区号码
    front_pool = {}
    for num, freq in frequent_front:
        front_pool[num] = front_pool.get(num, 0) + freq * 1.2  #近期开奖权重更高

    #后区号码
    back_pool = {}
    for num, freq in frequent_back:
        back_pool[num] = back_pool.get(num, 0) + freq * 1.2

    #选择前5个高频前区号码
    recommended_front = sorted(front_pool.items(), key=lambda x: x[1], reverse=True)[:5]
    recommended_front = [x[0] for x in recommended_front]

    #选择前2个高频后区号码
    recommended_back = sorted(back_pool.items(), key=lambda x: x[1], reverse=True)[:2]
    recommended_back = [x[0] for x in recommended_back]

    return {
        "推荐方案": {
            "前区号码": " ".join(sorted(recommended_front, key=int)),
            "后区号码": " ".join(sorted(recommended_back, key=int))
        },
        "预测开奖日期": "2025-07-02 (周三)",
        "预测销售额": f"{int(next_sale_prediction):,}元"
    }

recommendation = recommend_dlt_numbers()
print("大乐透号码推荐 (2025年7月2日):")
print(json.dumps(recommendation, indent=4, ensure_ascii=False))

#括号三
#前区号码频次和周几的关系
from pyecharts.charts import Timeline
timeline = Timeline()
bar31 = Bar()#周一的图
f_num_sorted = sorted(F_Mon_num.items(),key=lambda x:x[1],reverse=True)
f_x = []
f_y = []

for n in f_num_sorted:
    f_x.append(n[0])
    f_y.append(n[1])
bar31.add_xaxis(f_x)
bar31.add_yaxis("出现频次",f_y)
timeline.add(bar31,"周一")

bar33 = Bar()#周三的图
f_num_sorted = sorted(F_Wed_num.items(),key=lambda x:x[1],reverse=True)
f_x = []
f_y = []

for n in f_num_sorted:
    f_x.append(n[0])
    f_y.append(n[1])
bar33.add_xaxis(f_x)
bar33.add_yaxis("出现频次",f_y)
timeline.add(bar33,"周三")

bar36 = Bar()#周六的图
f_num_sorted = sorted(F_Sat_num.items(),key=lambda x:x[1],reverse=True)
f_x = []
f_y = []

for n in f_num_sorted:
    f_x.append(n[0])
    f_y.append(n[1])
bar36.add_xaxis(f_x)
bar36.add_yaxis("出现频次",f_y)
timeline.add(bar36,"周六")
timeline.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline.render("周一、周三、周六的前区号码频次统计.html")

#后区号码跟周几的关系
timeline2 = Timeline()
bar31 = Bar()#周一的图
b_num_sorted = sorted(B_Mon_num.items(),key=lambda x:x[1],reverse=True)
b_x = []
b_y = []
for n in b_num_sorted:
    b_x.append(n[0])
    b_y.append(n[1])
bar31.add_xaxis(b_x)
bar31.add_yaxis("出现频次",b_y)
timeline2.add(bar31,"周一")

bar33 = Bar()#周三的图
b_num_sorted = sorted(B_Wed_num.items(),key=lambda x:x[1],reverse=True)
b_x = []
b_y = []
for n in b_num_sorted:
    b_x.append(n[0])
    b_y.append(n[1])
bar33.add_xaxis(b_x)
bar33.add_yaxis("出现频次",b_y)
timeline2.add(bar33,"周三")

bar36 = Bar()#周六的图
b_num_sorted = sorted(B_Sat_num.items(),key=lambda x:x[1],reverse=True)
b_x = []
b_y = []
for n in b_num_sorted:
    b_x.append(n[0])
    b_y.append(n[1])
bar36.add_xaxis(b_x)
bar36.add_yaxis("出现频次",b_y)
timeline2.add(bar36,"周六")
timeline2.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline2.render("周一、周三、周六的后区号码频次统计.html")


line3 = Line()
line3.add_xaxis(["周一","周三","周六"])
line3.add_yaxis("平均总销售额",Sum)
line3.render("周一、周三、周六总销售额平均值比较.html")


#括号四
from pyecharts.options import *
age = []
article_num = []
for p in expert_data:
    if p['彩龄'] not in age:
        age.append(p['彩龄'] )
    if p['发文量'] not in article_num:
        article_num.append(p['发文量'] )
age.sort()
article_num.sort()
#彩龄和大乐透
timeline3 = Timeline()
for p_age in age:
    bar4 = Bar()
    bar4.add_xaxis(["一等奖","二等奖","三等奖"])
    y_num = [0.0]*3

    for p in expert_data:
        if p['彩龄'] != p_age:
            continue
        if p['大乐透中奖情况'][4] == "N":
            continue
        s = p['大乐透中奖情况'].replace("一等奖:","").replace("二","").replace("三","").split("等奖:")
        num = []
        for str in s:
            num.append(int(str))

        y_num[0] = (y_num[0] + num[0])/2
        y_num[1] = (y_num[1] + num[1]) / 2
        y_num[2] = (y_num[2] + num[2]) / 2
    bar4.add_yaxis("平均中奖次数",y_num)
    bar4.set_global_opts(title_opts=TitleOpts(is_show=True,title=f"彩龄为{p_age}的专家大乐透中奖情况"))
    timeline3.add(bar4,f"彩龄为{p_age}")
timeline3.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline3.render("彩龄与大乐透中奖情况的关系.html")

#彩龄和双色球
timeline3 = Timeline()
for p_age in age:
    bar4 = Bar()
    bar4.add_xaxis(["一等奖","二等奖","三等奖"])
    y_num = [0.0]*3

    for p in expert_data:
        if p['彩龄'] != p_age:
            continue
        if p['双色球中奖情况'][4] == "N":
            continue
        s = p['双色球中奖情况'].replace("一等奖:","").replace("二","").replace("三","").split("等奖:")
        num = []
        for str in s:
            num.append(int(str))

        y_num[0] = (y_num[0] + num[0])/2
        y_num[1] = (y_num[1] + num[1]) / 2
        y_num[2] = (y_num[2] + num[2]) / 2
    bar4.add_yaxis("平均中奖次数",y_num)
    bar4.set_global_opts(title_opts=TitleOpts(is_show=True,title=f"彩龄为{p_age}的专家双色球中奖情况"))

    timeline3.add(bar4,f"彩龄为{p_age}")
timeline3.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline3.render("彩龄与双色球中奖情况的关系.html")

#发文量和大乐透
timeline3 = Timeline()
for p_num in article_num:
    bar4 = Bar()
    bar4.add_xaxis(["一等奖","二等奖","三等奖"])
    y_num = [0.0]*3

    for p in expert_data:
        if p['发文量'] != p_num:
            continue
        if p['大乐透中奖情况'][4] == "N":
            continue
        s = p['大乐透中奖情况'].replace("一等奖:","").replace("二","").replace("三","").split("等奖:")
        num = []
        for str in s:
            num.append(int(str))

        y_num[0] = (y_num[0] + num[0])/2
        y_num[1] = (y_num[1] + num[1]) / 2
        y_num[2] = (y_num[2] + num[2]) / 2
    bar4.add_yaxis("平均中奖次数",y_num)
    bar4.set_global_opts(title_opts=TitleOpts(is_show=True,title=f"发文量为{p_num}的专家大乐透中奖情况"))
    timeline3.add(bar4,f"发文量为{p_num}")
timeline3.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline3.render("发文量与大乐透中奖情况的关系.html")

#发文量和双色球
timeline3 = Timeline()
for p_num in article_num:
    bar4 = Bar()
    bar4.add_xaxis(["一等奖","二等奖","三等奖"])
    y_num = [0.0]*3

    for p in expert_data:
        if p['发文量'] != p_num:
            continue
        if p['双色球中奖情况'][4] == "N":
            continue
        s = p['双色球中奖情况'].replace("一等奖:","").replace("二","").replace("三","").split("等奖:")
        num = []
        for str in s:
            num.append(int(str))

        y_num[0] = (y_num[0] + num[0])/2
        y_num[1] = (y_num[1] + num[1]) / 2
        y_num[2] = (y_num[2] + num[2]) / 2
    bar4.add_yaxis("平均中奖次数",y_num)
    bar4.set_global_opts(title_opts=TitleOpts(is_show=True,title=f"发文量为{p_num}的专家双色球中奖情况"))

    timeline3.add(bar4,f"发文量为{p_num}")
timeline3.add_schema(
    play_interval=1000,
    is_timeline_show = True,
    is_auto_play=True,
    is_loop_play=True
)
timeline3.render("发文量与双色球中奖情况的关系.html")

