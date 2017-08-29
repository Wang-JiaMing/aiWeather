# import weatherHtml
import mail
import weatherModel
import weatherforecast
import weatherWarning
import dataBase
import mailModel
import pytz
import datetime

mailAddressList = ['13422192925@163.com']  # , '601229570@qq.com', '352294249@qq.com']


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
    sql = 'select * from weather w,weatherlife wl where w.status="1" or w.autoTips="1" and  w.id=wl.wid order by w.create_date desc limit 0,1'
    wm = ''
    for row in dataBase.getDataAll(sql):
        wm = weatherModel.weatherModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                       row[10], row[11], row[12], row[13], row[16], row[17], row[18], row[19], row[20],
                                       row[21], row[22], row[23])
    return wm


def getNewWeatherMsg():
    sql = 'select * from weather w,weatherlife wl where w.id=wl.wid order by  wl.create_date DESC LIMIT 0,1'
    wm = ''
    for row in dataBase.getDataAll(sql):
        wm = weatherModel.weatherModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                       row[10], row[11], row[12], row[13], row[16], row[17], row[18], row[19], row[20],
                                       row[21], row[22], row[23])
    return wm


def getNewForecast(id):
    sql = 'select * from weatherforecast wf where wf.wId="' + id + '" order by f_index asc'
    weatherforecastList = []
    for row in dataBase.getDataAll(sql):
        weatherforecastList.append(weatherforecast.weatherforecast(row[2], row[3], row[4], row[5], row[6]))
    return weatherforecastList


def getWarning(id):
    sql = 'select * from weatherwarning wf where wf.wId="' + id + '"'
    warnList = []
    for row in dataBase.getDataAll(sql):
        warnList.append(weatherWarning.weatherWarning(row[2], row[3], row[4], row[5], row[6]))
    return warnList


def everyDaySend():
    oid = getNewMailId()
    weather = getNewWeatherMsg()
    if oid != weather.id:
        forecast = getNewForecast(weather.id)
        warning = getWarning(weather.id)
        title = 'X.M Tips天气早报:' + forecast[0].situation + ' 气温 ' + forecast[0].temperature + " " + weather.warning
        content = mailModel.everyDayModel(weather, forecast, warning)
        i = 0
        while i < len(mailAddressList):
            mail.sendMail(title, content, mailAddressList[i])
            i += 1
        if oid != '':
            dataBase.update('update weather t set t.status="0" where t.id="' + oid + '"')
        dataBase.update('update weather t set t.status="1" where t.id="' + weather.id + '"')
    else:
        print("[" + getTime() + "]不重复发送")


def autoWeather():
    nw = getNewWeatherMsg()
    if nw.autoTips != 1 and nw.status != 1 and (int(getHouse()) < 22 or int(getHouse()) > 7):
        oldWeather = getOldSendWeather()
        oldWarning = getWarning(oldWeather.id)
        nowForecast = ''
        nowWarning = ''
        content = ''

        nWarning = getWarning(nw.id)
        nWarnIndex = 0
        tipsType = 0
        if len(nWarning) > 0:
            while nWarnIndex < len(nWarning):
                oWarnIndex = 0

                while oWarnIndex < len(oldWarning):
                    if nWarning[nWarnIndex].warnTitle != oldWarning[oWarnIndex].warnTitle:
                        tipsType += 1
                    oWarnIndex += 1

                if tipsType == len(oldWarning):
                    tipsType = -1
                    break
                nWarnIndex += 1

        if oldWeather.temperature - nw.temperature <= -5 or oldWeather.temperature - nw.temperature >= 5 or \
                (oldWeather.weather_condition != nw.weather_condition and oldWeather.weather_condition != nw.weather_condition and nw.weather_condition.find(
                        '晴') == -1 and nw.weather_condition.find('多云') == -1 and nw.weather_condition.find(
            '阴') == -1) or tipsType == -1:
            nForecast = getNewForecast(nw.id)
            title = "X.M Auto Tips: "
            content = ''
            if oldWeather.temperature - nw.temperature <= -5 or oldWeather.temperature - nw.temperature >= 5:
                title += '温差过大! '
                content += '温差' + str(int(oldWeather.temperature) - int(nw.temperature)) + '℃'
                if oldWeather.temperature - nw.temperature <= -5:
                    content += ',请注意保暖'
                content += ';'
            if oldWeather.weather_condition != nw.weather_condition and nw.weather_condition.find(
                    '晴') == -1 and nw.weather_condition.find('多云') == -1 and nw.weather_condition.find('阴') == -1:
                title += '天气有变化(' + oldWeather.weather_condition + '-->' + nw.weather_condition + ')! '
                if nw.weather_condition.find('雨') > -1:
                    content += '天气转变[' + oldWeather.weather_condition + '-->' + nw.weather_condition + ']，记得带伞;'
                elif nw.weather_condition.find('雷') > -1:
                    content += '天气转变[' + oldWeather.weather_condition + '-->' + nw.weather_condition + ']，主要防雷;'
            if tipsType == -1:
                title += '预警信号有变(' + nw.warning + ')!'
                content += '预警信号有变动,注意查看以下预警信息内容;'
            i = 0
            while i < len(mailAddressList):
                mail.sendMail(title, mailModel.autoModel(content, nw, nForecast, nWarning), mailAddressList[i])
                i += 1
            dataBase.update('update weather t set t.autoTips="1" where t.id="' + str(id) + '"')
        else:
            print("[" + getTime() + "]没新提示内容")
    else:
        print("[" + getTime() + "]自动提示条件不满足，不给予提示")
