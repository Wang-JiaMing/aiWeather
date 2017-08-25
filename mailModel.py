#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytz
import datetime


def getTime():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


def everyDayModel(weather, forecast, warning):
    content = ''
    content += '[总体情况]' + weather.weatherModel.overview + '\n\n'
    content += '[地点]' + weather.weatherModel.province + " " + weather.weatherModel.county + '\n'
    content += '------ 当前情况 ------\n'
    content += '[温度]' + str(weather.weatherModel.temperature) + "℃\n"
    content += "[Pm2.5]" + weather.weatherModel.pm25 + "\n"
    content += "[天气]" + weather.weatherModel.weather_condition + "\n"
    content += "[湿度]" + weather.weatherModel.humidity + '\n'
    content += "[风向]" + weather.weatherModel.wind_direction + '\n'

    if len(warning.weatherWarning.warnTitle) > 0:
        content += '------ 现悬挂预警信号 -----\n'
        windex = 0
        while windex < len(warning.weatherWarning.warnTitle):
            content += warning.weatherWarning.warnTitle[windex] + '\n'
            content += '[悬挂时间]' + warning.weatherWarning.warnDate[windex] + '\n'
            content += '[预警内容]' + warning.weatherWarning.warnContent[windex] + '\n'
            content += '[预警解析]' + warning.weatherWarning.warnAnalysis[windex] + '\n'
            content += '[预警提示]' + warning.weatherWarning.warnTips[windex] + '\n\n'
            windex += 1
    content += '------ 未来3天预测 -----\n'
    findex = 0
    while findex < 3:
        content += str(forecast.weatherforecast.f_index[findex]) + ". [" + forecast.weatherforecast.f_time[findex] + \
                   "] 天气状况:" + forecast.weatherforecast.situation[findex] + \
                   " 最低/最高温度:" + forecast.weatherforecast.temperature[findex] + \
                   " 风向:" + forecast.weatherforecast.wind_direction[findex] + '\n\n'
        findex += 1
    content += '\n\n'
    content += '                        FROM X.M Tips Server\n'
    content += '                        ' + getTime()
    return content


def autoModel(autoMsg, weather, forecast, warning):
    content = ''
    content += '[智能提示]' + autoMsg + '\n\n'
    content += '[地点]' + weather.weatherModel.province + " " + weather.weatherModel.county + '\n'
    content += '------ 当前情况 ------\n'
    content += '[温度] ' + str(weather.weatherModel.temperature) + "℃\n"
    content += "[Pm2.5]" + weather.weatherModel.pm25 + "\n"
    content += "[天气] " + weather.weatherModel.weather_condition + "\n"
    content += "[湿度] " + weather.weatherModel.humidity + '\n'
    content += "[风向] " + weather.weatherModel.wind_direction + '\n'

    if len(warning.weatherWarning.warnTitle) > 0:
        content += '------ 现悬挂预警信号 -----\n'
        windex = 0
        while windex < len(warning.weatherWarning.warnTitle):
            content += warning.weatherWarning.warnTitle[windex] + '\n'
            content += '[悬挂时间]' + warning.weatherWarning.warnDate[windex] + '\n'
            content += '[预警内容]' + warning.weatherWarning.warnContent[windex] + '\n'
            content += '[预警解析]' + warning.weatherWarning.warnAnalysis[windex] + '\n'
            content += '[预警提示]' + warning.weatherWarning.warnTips[windex] + '\n\n'
            windex += 1
    content += '\n\nPS:为什么会收到该邮件?当温差距离上次提醒超过5℃或天气转变或预警信号有变化,即会发送通知提醒!'
    content += '\n\n'
    content += '                        FROM X.M Tips Server\n'
    content += '                        ' + getTime()
    return content
