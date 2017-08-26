# import weatherHtml
import mail
import weatherModel
import weatherforecast
import weatherWarning
import dataBase
import mailModel
import pytz
import datetime

mailAddressList = ['13422192925@163.com', '601229570@qq.com', '352294249@qq.com']


def getTime():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def getHouse():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%H')


def getNewMailId():
    sql = 'select id from weather  where status="1"'
    return dataBase.getDataforOne(sql)


def getSendWeather():
    sql = 'select * from weather  where status="1"'
    w = weatherModel
    for row in dataBase.getDataAll(sql):
        w.weatherModel.temperature = row[4]
        w.weatherModel.weather_condition = row[5]
        w.weatherModel.warning = row[11]
    return w


def getOldSendWeather():
    sql = 'select * from weather where status="1" or autoTips="1" order by create_date desc limit 0,1'
    w = weatherModel
    for row in dataBase.getDataAll(sql):
        w.weatherModel.temperature = row[4]
        w.weatherModel.weather_condition = row[5]
        w.weatherModel.warning = row[11]
    return w

def getNewWeatherMsg():
    sql = 'select * from weather w,weatherlife wl where w.id=wl.wid order by  wl.create_date DESC LIMIT 0,1'
    wm = weatherModel
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
        wm.weatherModel.status = row[12]
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
    wf = weatherforecast
    for row in dataBase.getDataAll(sql):
        wf.weatherforecast.f_index.append(row[2])
        wf.weatherforecast.f_time.append(row[3])
        wf.weatherforecast.situation.append(row[4])
        wf.weatherforecast.temperature.append(row[5])
        wf.weatherforecast.wind_direction.append(row[6])
    return wf


def getNewWarning(id):
    sql = 'select * from weatherwarning wf where wf.wId="' + id + '"'
    ww = weatherWarning
    for row in dataBase.getDataAll(sql):
        ww.weatherWarning.warnTitle.append(row[2])
        ww.weatherWarning.warnDate.append(row[3])
        ww.weatherWarning.warnContent.append(row[4])
        ww.weatherWarning.warnAnalysis.append(row[5])
        ww.weatherWarning.warnTips.append(row[6])
    return ww


def everyDaySend():
    oid = getNewMailId()
    weather = getNewWeatherMsg()
    if oid != weather.weatherModel.id:
        forecast = getNewForecast(weather.weatherModel.id)
        warning = getNewWarning(weather.weatherModel.id)
        title = 'X.M Tips天气早报:' + forecast.weatherforecast.situation[0] + ' 气温 ' + forecast.weatherforecast.temperature[
            0] + " " + weather.weatherModel.warning
        content = mailModel.everyDayModel(weather, forecast, warning)
        i = 0
        while i < len(mailAddressList):
            mail.sendMail(title, content, mailAddressList[i])
            i += 1
        if oid != '':
            dataBase.update('update weather t set t.status="0" where t.id="' + oid + '"')
        dataBase.update('update weather t set t.status="1" where t.id="' + weather.weatherModel.id + '"')
    else:
        print("["+getTime()+"]不重复发送")

def autoWeather():
    autoTips = getNewWeatherMsg().weatherModel.autoTips
    status = getNewWeatherMsg().weatherModel.status
    if autoTips != 1 and status != 1 :
        sendTem = getOldSendWeather().weatherModel.temperature
        sendCondition = getOldSendWeather().weatherModel.weather_condition
        sendWarning = getOldSendWeather().weatherModel.warning
        _tmp = getNewWeatherMsg().weatherModel.temperature
        _warning = getNewWeatherMsg().weatherModel.warning
        _condition = getNewWeatherMsg().weatherModel.weather_condition
        id = getNewWeatherMsg().weatherModel.id
        nowWeather = getNewWeatherMsg()
        nowForecast = ''
        nowWarning = ''
        content = ''
        if sendTem - _tmp <= -5 or sendTem - _tmp >= 5 or sendCondition != _condition or sendWarning != _warning:
            nowForecast = getNewForecast(id)
            nowWarning = getNewWarning(id)
            title = "X.M Auto Tips: "
            content = ''
            if sendTem - _tmp <= -5 or sendTem - _tmp >= 5:
                title += '温差过大! '
                content += '温差' + str(int(sendTem) - int(_tmp)) + '℃'
                if sendTem - _tmp <= -5:
                    content += ',请注意保暖'
                content += ';'
            if sendCondition != _condition:
                title += '天气有变化(' + sendCondition + '=>' + _condition + ')! '
                if _condition.find('雨') > -1:
                    content += '天气转变[' + sendCondition + '=>' + _condition + ']，记得带伞;'
                if _condition.find('晴') > -1:
                    content += '天气转变[' + sendCondition + '=>' + _condition + ']，注意防晒;'
            if sendWarning != _warning:
                title += '预警信号有变(' + _warning + ')!'
                content += '预警信号有变动,注意查看以下预警信息内容;'
            # print(mailModel.autoModel(content, nowWeather, nowForecast, nowWarning))
            i = 0
            while i < len(mailAddressList):
                mail.sendMail(title, mailModel.autoModel(content, nowWeather, nowForecast, nowWarning),mailAddressList[i])
                i += 1
            dataBase.update('update weather t set t.autoTips="1" where t.id="' + id + '"')
        else:
            print("[" + getTime() + "]没新提示内容")
    else:
        print("[" + getTime() + "]自动提示条件不满足，不给予提示")
