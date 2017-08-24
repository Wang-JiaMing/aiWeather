# -*- coding:utf-8 -*-
import urllib.request
import uuid

from bs4 import BeautifulSoup

import dataBase


def getSoup(url):
    # 请求
    request = urllib.request.Request(url)
    # 爬取结果
    response = urllib.request.urlopen(request)
    data = response.read()
    # 设置解码方式
    data = data.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    return soup


def insertWeatherMsg():
    listSql = []
    _uuid = str(uuid.uuid4())
    soup = getSoup("https://tianqi.moji.com/weather/china/guangdong/nansha-district");
    sql = 'insert into weather(id,overview,province,county,pm25,warning,temperature,weather_condition,humidity,wind_direction,msg_update_time) values("' + _uuid + '",'
    sql += '"' + soup.find_all('meta')[2]['content'].replace('墨迹天气', '小明同学') + '",'
    sql += '"' + soup.find_all('em')[0].string.split('，')[1] + '",'
    sql += '"' + soup.find_all('em')[0].string.split('，')[0] + '",'
    sql += '"' + soup.find(attrs={'class': 'wea_alert clearfix'}).em.string + '",'
    weatherWarning = soup.find(attrs={'class': 'warning_aqi'})
    if weatherWarning != None:
        sql += '"' + weatherWarning.select('em')[0].string + '",'
        warningLink = ''
        for link in weatherWarning.select('a'):
            warningLink = link.get('href')
        warningSoup = getSoup(warningLink)
        warningContent = warningSoup.find_all(class_='warning_box')
        warnIndex = 0
        while warnIndex < len(warningContent):
            _wuuid = str(uuid.uuid4())
            wsql = 'insert into weatherwarning(id,wid,warnTitle,warnDate,warnContent,warnAnalysis,warnTips)VALUES ("' + _wuuid + '","' + _uuid + '",'
            wsql += '"' + warningContent[warnIndex].find_all('h1')[0].string + '",'
            wsql += '"' + warningContent[warnIndex].find_all('span')[0].string.split('：')[1] + '",'
            wsql += '"' + warningContent[warnIndex].find_all(class_='warning_title_sub')[0].string + '",'
            wsql += '"' + warningContent[warnIndex].find_all('li')[2].string.split('：')[1] + '","'
            liIndex = 3
            while liIndex < len(warningContent[warnIndex].find_all('li')):
                wsql += warningContent[warnIndex].find_all('li')[liIndex].string
                liIndex += 1
            wsql += '")'
            warnIndex += 1
            listSql.insert(len(listSql), wsql)
    else:
        sql += '"",'

    # 摄氏度+天气情况
    ssd = soup.find(attrs={'class': 'wea_weather clearfix'})
    # 湿度+风向
    sd_fx = soup.find(attrs={'class': 'wea_about clearfix'})
    sql += '"' + ssd.em.string + '",'
    sql += '"' + ssd.b.string + '",'
    sql += '"' + sd_fx.span.string + '",'
    sql += '"' + sd_fx.em.string + '",'
    nowTime = ssd.strong.string
    sql += '"' + ssd.strong.string + '")'
    dataTime = dataBase.getDataforOne(
        "select msg_update_time From weather w where to_days(w.create_date) = to_days(now()) LIMIT 0,1")
    if dataTime != nowTime:
        listSql.insert(len(listSql), sql)
        tqyb = soup.find(attrs={'class': 'forecast clearfix'}).select('ul')
        i = 1
        while i < len(tqyb):
            _fuuid = str(uuid.uuid4())
            fsql = 'insert into weatherforecast(id,wId,f_index,f_time,situation,temperature,wind_direction)VALUES ("' + _fuuid + '","' + _uuid + '","' + str(
                i) + '",'
            fsql += '"' + tqyb[i].find_all('li')[0].a.string + '",'
            fsql += '"' + tqyb[i].find_all('li')[1].get_text(strip=True) + '",'
            fsql += '"' + tqyb[i].find_all('li')[2].string + '",'
            fsql += '"' + tqyb[i].find_all('li')[3].em.string + tqyb[i].find_all('li')[3].b.string + '")'
            i += 1
            listSql.insert(len(listSql), fsql)

        live = soup.find(attrs={'class': 'live_index_grid'}).select('li')
        ii = 0
        _luuid = str(uuid.uuid4())
        lsql = 'INSERT  into weatherlife(id,wid,makeup,cold,car_wash,air_pollution,dress,ultraviolet_rays,sport,go_fishing)VALUES ("' + _luuid + '","' + _uuid + '",'
        while ii < len(live):
            if live[ii].dd != None:
                lsql += '"' + live[ii].dt.string
                if ii == 7:
                    lsql += '")'
                else:
                    lsql += '",'
            ii += 1
        listSql.insert(len(listSql), lsql)
        dataBase.insertManySql(listSql)
    else:
        print("与服务器时间相同，不更新")


insertWeatherMsg()
