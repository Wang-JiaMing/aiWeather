# -*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

def getSoup():
    # 网址
    url = "https://tianqi.moji.com/weather/china/guangdong/nansha-district"
    # 请求
    request = urllib.request.Request(url)
    # 爬取结果
    response = urllib.request.urlopen(request)
    data = response.read()
    # 设置解码方式
    data = data.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def getWeatherMsg():
    soup = getSoup();
    weatherConntent = ''
    weatherConntent += '[概览]' + soup.find_all('meta')[2]['content'].replace('墨迹天气', '小明同学') + '\n\n'
    weatherConntent += '服务器所在地区:' + soup.find_all('em')[0].string + '\n\n'
    weatherConntent += '空气质量(pm2.5):' + soup.find(attrs={'class': 'wea_alert clearfix'}).em.string + '\n\n'

    # 预警信号
    weatherWarning = soup.find(attrs={'class': 'warning_aqi'})
    if weatherWarning != None:
        weatherConntent += '现悬挂' + weatherWarning.select('em')[0].string + '预警信号\n\n'

    # 摄氏度+天气情况
    ssd = soup.find(attrs={'class': 'wea_weather clearfix'})
    # 湿度+风向
    sd_fx = soup.find(attrs={'class': 'wea_about clearfix'})
    # 今日提示
    weatherConntent += '--------现在情况--------\n'
    weatherConntent += '温度:' + ssd.em.string + '℃\n\n'
    weatherConntent += '天气情况:' + ssd.b.string + '\n\n'
    weatherConntent += sd_fx.span.string + '\n\n'
    weatherConntent += sd_fx.em.string + '\n\n'
    weatherConntent += '天气更新时间:' + ssd.strong.string + '\n\n'
    weatherConntent += '--------天气预报--------\n'
    tqyb = soup.find(attrs={'class': 'forecast clearfix'}).select('ul')
    i = 1
    while i < len(tqyb):
        weatherConntent += tqyb[i].find_all('li')[0].a.string + ' ' + tqyb[i].find_all('li')[1].get_text(
            strip=True) + ' ' + \
                           tqyb[i].find_all('li')[2].string + '(最低温度/最高温度) ' + tqyb[i].find_all('li')[3].em.string + \
                           tqyb[i].find_all('li')[3].b.string + '\n\n'
        i += 1

    weatherConntent += '--------生活指栏--------\n'
    live = soup.find(attrs={'class': 'live_index_grid'}).select('li')
    ii = 0

    while ii < len(live):
        if live[ii].dd != None:
            weatherConntent += live[ii].dd.string + ':' + live[ii].dt.string + '\n\n'
        ii += 1
    print(weatherConntent)
    return weatherConntent


def getWeatherTitle():
    soup = getSoup()
    tip = soup.find(attrs={'class': 'wea_tips clearfix'})
    return tip.em.string

getWeatherMsg()