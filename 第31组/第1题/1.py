import requests
import json
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
import re

from pyecharts.options import VisualMapOpts


def crawl_hurun_rich_list():
# 模拟浏览器请求头
    headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
         'Accept': 'application/json, text/javascript, */*; q=0.01',
         'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
         'Referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails',
         'X-Requested-With': 'XMLHttpRequest',
         'Sec-Fetch-Dest': 'empty',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Site': 'same-origin',
         'Connection': 'keep-alive',
         'Pragma': 'no-cache',
         'Cache-Control': 'no-cache',
         'TE': 'trailers'
     }
     # 榜单数据接口（需根据实际页面更新num参数）
    url = "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"
    all_data = []
    page_size = 100
    offset = 0
    while True:
        params = {
            'num': 'ODBYW2BI',  # 2024年榜单标识（需确认）
            'offset': offset,
            'limit': page_size
                }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code != 200:
                print(f"请求失败: {response.status_code}")
                break
            data = response.json()
            items = data.get('rows', [])
            if not items:
                break
            all_data.extend(items)
            offset += page_size
            print(f"已获取 {len(items)} 条数据，总计 {len(all_data)} 条")
            # 随机延时防止反爬
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"爬取失败: {str(e)}")
            break
# 数据解析
    processed_data = []
    for item in all_data:
        chara = item['hs_Character'][0]
        processed_data.append({
          '排名': item.get('hs_Rank_Rich_Ranking'),
          '姓名': item.get('hs_Rank_Rich_ChaName_Cn'),
          '财富(亿元)': item.get('hs_Rank_Rich_Wealth'),
          '年龄': chara.get('hs_Character_Age'),
          '性别': chara.get('hs_Character_Gender_Lang'),
          '公司': item.get('hs_Rank_Rich_ComName_Cn'),
          '行业': item.get('hs_Rank_Rich_Industry_Cn'),
          '总部': item.get('hs_Rank_Rich_ComHeadquarters_Cn'),
          '出生地': chara.get('hs_Character_BirthPlace_Cn')
            })
    # df = pd.DataFrame(processed_data)
    # df.to_csv('2024胡润百富榜.csv', index=False, encoding='utf_8_sig')
    return processed_data










    # 执行爬虫
df = crawl_hurun_rich_list()

#括号二
from pyecharts.charts import Bar
import  pyecharts.options as opts
count_p = {}#不同行业人数
count_m = {}#不同行业财富
count_man:int = 0#统计男性数量
count_woman:int = 0
# min_age = 1000     最小年龄33
# max_age = 0        最大年龄107
age_garde:[int] = [0]*9#统计各年龄分级人数
province_data = {}   #统计省份信息

for p in df:
    # if p['出生地'] != "":
    #     print(p['出生地'].split("-"))
    try:
       count_p[p['行业']] = count_p[p['行业']] +1
    except:
        count_p[p['行业']] = 1
    try:
        count_m[p['行业']] = count_m[p['行业']] + p['财富(亿元)']
    except:
        count_m[p['行业']] = p['财富(亿元)']
    if p['性别'] =='先生':
        count_man = count_man + 1
    else:
        count_woman = count_woman+1

#     try:
#         if int(p['年龄']) < min_age:
#             min_age = int(p['年龄'])
#         if int(p['年龄']) > max_age:
#             max_age = int(p['年龄'])
#     except:
#         print(p['年龄'])
#         continue
#
# print(f"!!!!!!!!!!最小年龄为：{min_age}")
# print((f"最大年龄为：{max_age}"))
    if p['年龄'] == '未知':
        age_garde[8] = age_garde[8] + 1
    elif int(p['年龄']) <40 :
        age_garde[0] = age_garde[0] + 1
    elif int(p['年龄']) <50 :
        age_garde[1] = age_garde[1] + 1
    elif int(p['年龄']) <60 :
        age_garde[2] = age_garde[2] + 1
    elif int(p['年龄']) <70 :
        age_garde[3] = age_garde[3] + 1
    elif int(p['年龄']) <80 :
        age_garde[4] = age_garde[4] + 1
    elif int(p['年龄']) <90 :
        age_garde[5] = age_garde[5] + 1
    elif int(p['年龄']) <100 :
        age_garde[6] = age_garde[6] + 1
    elif int(p['年龄']) <110 :
        age_garde[7] = age_garde[7] + 1
    try:
        if p['出生地'] != '':
            dir_list =  p['出生地'].split("-")
            if dir_list[0] == '中国':
                province_name = dir_list[1]
                if province_name in ['北京','重庆','上海','天津']:
                    province_name = province_name + '市'
                elif province_name in ['内蒙古','西藏']:
                    province_name = province_name + '自治区'
                elif province_name == '宁夏':
                    province_name = province_name + '回族自治区'
                elif province_name == '新疆':
                    province_name = province_name + '维吾尔自治区'
                elif province_name == '广西':
                    province_name = province_name + '壮族自治区'
                elif province_name in ['香港', '澳门']:
                    province_name = province_name + '特别行政区'
                else:
                    province_name = province_name + '省'
                province_data[province_name] =  province_data[province_name] + 1
    except:
        dir_list = p['出生地'].split("-")
        if dir_list[0] == '中国':
            province_name = dir_list[1]
            if province_name in ['北京', '重庆', '上海', '天津']:
                province_name = province_name + '市'
            elif province_name in ['内蒙古', '西藏']:
                province_name = province_name + '自治区'
            elif province_name == '宁夏':
                province_name = province_name + '回族自治区'
            elif province_name == '新疆':
                province_name = province_name + '维吾尔自治区'
            elif province_name == '广西':
                province_name = province_name + '壮族自治区'
            elif province_name in ['香港','澳门']:
                province_name = province_name + '特别行政区'
            else:
                province_name = province_name + '省'
            province_data[province_name] = 1

sorted_items = sorted(count_p.items(), key=lambda item: item[1], reverse=True)

sorted_cp= dict(sorted_items)

sorted_items = sorted(count_m.items(), key=lambda item: item[1], reverse=True)
sorted_cm= dict(sorted_items)



bar = Bar()
x1:[str] = []
y1:[str] = []
for a in sorted_cp.keys():
    if sorted_cp[a] <=2:
        continue
    x1.append(str(a))
    y1.append(str(count_p[a]))
bar.add_xaxis(x1)
bar.add_yaxis("各行业富豪人数",y1)
bar.set_global_opts(
    datazoom_opts=[opts.DataZoomOpts()]  # 添加滚动条
)
bar.render("各行业富豪人数.html")

bar2 = Bar()
x2:[str] = []
y2:[str] = []
for a in sorted_cm.keys():
    x2.append(str(a))
    y2.append(str(count_m[a]))

bar2.add_xaxis(x2)
bar2.add_yaxis("各行业富豪总财富",y2)
bar2.set_global_opts(
    datazoom_opts=[opts.DataZoomOpts()]  # 添加滚动条
)
bar2.render("各行业富豪总财富.html")

#括号三
##性别统计
#from pyecharts import options as opts
from pyecharts import options
from pyecharts.charts import Pie

pie_data = [('先生',count_man),('女士',count_woman)]
pie = Pie()
pie.add("",pie_data)
pie.set_global_opts(title_opts=opts.TitleOpts(title='中国前1000名富豪性别比例'))
pie.render("中国前1094名富豪性别比例.html")

##年龄统计
bar3 = Bar()
bar3.add_xaxis(["30-40","40,50","50-60","60-70","70-80","80-90","90-100","大于100","未知"])
bar3.add_yaxis("人数",age_garde)
bar3.set_global_opts(title_opts=opts.TitleOpts(title="不同年龄段的人数"))
bar3.render("中国前1094名富豪年龄分级统计.html")

##出生地统计
from pyecharts.charts import Map

province_data_list = list(province_data.items())
map = Map()
map.add("各省份诞生富豪人数",province_data_list,"china")
map.set_global_opts(
    title_opts=opts.TitleOpts(title="中国前1094名富豪出生地统计"),
    visualmap_opts= opts.VisualMapOpts(
        is_show=True,        #是否显示
        is_piecewise=True,   #是否分段
        pieces=[
            {"min":1,"max":9,"lable":"1~9人","color":"#CCFFFF"},
            {"min":10,"max":19,"lable":"10~19人","color":"#FFFF99"},
            {"min":20,"max":39,"lable":"20~39人","color":"#FF9966"},
            {"min":40,"max":59,"lable":"40~59人","color":"#FF6666"},
            {"min":60,"max":79,"lable":"60~79人","color":"#CC3333"},
            {"min":80,"lable":"80+人","color":"#990033"}
        ]
    )
)
map.render("中国前1094名富豪出生地统计.html")