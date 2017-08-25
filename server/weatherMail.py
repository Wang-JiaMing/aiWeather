# import weatherHtml
from server import mail
import pojo.weatherModel
import pojo.weatherWarning
import pojo.weatherforecast
import server.mailModel
from server import dataBase
import time

mailAddressList = ['13422192925@163.com']
autoMsg = ['温差≥5℃', '预警信号', '天气转变']


def getNewMailId():
    sql = 'select id from weather  where status="1"'
    return dataBase.getDataforOne(sql)


def getSendWeather():
    sql = 'select * from weather  where status="1"'
    w = pojo.weatherModel
    for row in dataBase.getDataAll(sql):
        w.weatherModel.temperature = row[4]
        w.weatherModel.weather_condition = row[5]
        w.weatherModel.warning = row[11]
    return w


def getNewWeatherMsg():
    sql = 'select * from weather w,weatherlife wl where w.id=wl.wid order by  wl.create_date DESC LIMIT 0,1'
    wm = pojo.weatherModel
    for row in dataBase.getDataAll(sql):
        wm.weatherModel.id = row[0]
        wm.weatherModel.overview = row[1]
        wm.weatherModel.province = row[2]
        wm.weatherModel.county = row[3]
        wm.weatherModel.temperature = row[4]
        wm.weatherModel.weather_condition = row[5]
        wm.weatherModel.humidity = row[6]
        wm.weatherModel.wind_direction = row[7]
        wm.weatherModel.msg_update_time = row[8]
        wm.weatherModel.pm25 = row[10]
        wm.weatherModel.warning = row[11]
        wm.weatherModel.autoTips = row[13]
        wm.weatherModel.makeup = row[16]
        wm.weatherModel.cold = row[17]
        wm.weatherModel.car_wash = row[18]
        wm.weatherModel.air_pollution = row[19]
        wm.weatherModel.dress = row[20]
        wm.weatherModel.ultraviolet_rays = row[21]
        wm.weatherModel.sport = row[22]
        wm.weatherModel.go_fishing = row[23]
    return wm


def getNewForecast(id):
    sql = 'select * from weatherforecast wf where wf.wId="' + id + '" order by f_index asc'
    wf = pojo.weatherforecast
    for row in dataBase.getDataAll(sql):
        wf.weatherforecast.f_index.append(row[2])
        wf.weatherforecast.f_time.append(row[3])
        wf.weatherforecast.situation.append(row[4])
        wf.weatherforecast.temperature.append(row[5])
        wf.weatherforecast.wind_direction.append(row[6])
    return wf


def getNewWarning(id):
    sql = 'select * from weatherwarning wf where wf.wId="' + id + '"'
    ww = pojo.weatherWarning
    for row in dataBase.getDataAll(sql):
        ww.weatherWarning.warnTitle.append(row[2])
        ww.weatherWarning.warnDate.append(row[3])
        ww.weatherWarning.warnCountent.append(row[4])
        ww.weatherWarning.warnAnalysis.append(row[5])
        ww.weatherWarning.warnTips.append(row[5])
    return ww


def everyDaySend():
    oid = getNewMailId()
    weather = getNewWeatherMsg()
    if oid != weather.weatherModel.id:
        forecast = getNewForecast(weather.weatherModel.id)
        warning = getNewWarning(weather.weatherModel.id)
        title = '天气早报:' + forecast.weatherforecast.situation[0] + ' 气温 ' + forecast.weatherforecast.temperature[
            0] + " " + weather.weatherModel.warning
        content = server.mailModel.everyDayModel(weather, forecast, warning)
        i = 0
        while i < len(mailAddressList):
            mail.sendMail(title, content, mailAddressList[i])
            i += 1
        if oid != '':
            dataBase.update('update weather t set t.status="0" where t.id="' + oid + '"')
        dataBase.update('update weather t set t.status="1" where t.id="' + weather.weatherModel.id + '"')


def autoWeather():
    autoTips = getNewWeatherMsg().weatherModel.autoTips
    if autoTips != 1 and (int(time.strftime("%H", time.localtime())) < 21 or int(time.strftime("%H", time.localtime())) > 8):
        sendTem = getSendWeather().weatherModel.temperature
        sendCondition = getSendWeather().weatherModel.weather_condition
        sendWarning = getSendWeather().weatherModel.warning
        nowTmp = getNewWeatherMsg().weatherModel.temperature
        nowWarning = getNewWeatherMsg().weatherModel.warning
        nowCondition = getNewWeatherMsg().weatherModel.weather_condition
        id = getNewWeatherMsg().weatherModel.id
        nowWeather = getNewWeatherMsg()
        nowForecast = ''
        nowWarning = ''
        content = ''
        if sendTem - nowTmp <= -5 or sendTem - nowTmp >= 5 or sendCondition != nowCondition or sendWarning != nowWarning:
            dataBase.update('update weather t set t.autoTips="1" where t.id="' + id + '"')
            nowForecast = getNewForecast(id)
            nowWarning = getNewWarning(id)
            title = "X.M Auto Tips: "
            content = ''
            if sendTem - nowTmp <= -5 or sendTem - nowTmp >= 5:
                title += '温差过大! '
                content += '温差' + str(int(sendTem) - int(nowTmp)) + '℃'
                if sendTem - nowTmp <= -5:
                    content += ',请注意保暖'
                content += ';'
            if sendCondition != nowCondition:
                title += '天气有变化 ' + sendCondition + '=>' + nowCondition + ' ! '
                if nowCondition.find('雨') > -1:
                    content += '天气转变[' + sendCondition + '=>' + nowCondition + ']，记得带伞;'
                if nowCondition.find('晴') > -1:
                    content += '天气转变[' + sendCondition + '=>' + nowCondition + ']，注意防晒;'
            if sendWarning != nowWarning:
                title += '新预警信号!'
                content += '预警信号有变动,注意查看以下预警信息内容;'
            i = 0
            while i < len(mailAddressList):
                mail.sendMail(title, server.mailModel.autoModel(content, nowWeather, nowForecast, nowWarning),
                              mailAddressList[i])
                i += 1

        else:
            print('没新提示内容')
