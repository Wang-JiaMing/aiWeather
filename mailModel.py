#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytz
import datetime


def getTime():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


def everyDayModel(weather, forecast, warning):
    content = ''
    content += '[总体情况]' + weather.overview + '\n\n'
    content += '[地点]' + weather.province + " " + weather.county + '\n'
    content += '------ 当前情况 ------\n'
    content += '[温度]' + str(weather.temperature) + "℃\n"
    content += "[Pm2.5]" + weather.pm25 + "\n"
    content += "[天气]" + weather.weather_condition + "\n"
    content += "[湿度]" + weather.humidity + '\n'
    content += "[风向]" + weather.wind_direction + '\n'

    if len(warning) > 0:
        content += '------ 现悬挂预警信号 -----\n'
        windex = 0
        while windex < len(warning):
            content += warning[windex].warnTitle + '\n'
            content += '[悬挂时间]' + warning[windex].warnDate + '\n'
            content += '[预警内容]' + warning[windex].warnContent + '\n'
            content += '[预警解析]' + warning[windex].warnAnalysis + '\n'
            content += '[预警提示]' + warning[windex].warnTips + '\n\n'
            windex += 1
    content += '------ 未来3天预测 -----\n'
    findex = 0
    while findex < 3:
        content += str(forecast[findex].f_index) + ". [" + forecast[findex].f_time + \
                   "] 天气状况:" + forecast[findex].situation + \
                   " 最低/最高温度:" + forecast[findex].temperature + \
                   " 风向:" + forecast[findex].wind_direction + '\n\n'
        findex += 1
    content += '\n\n'
    content += '                        FROM X.M Tips Server\n'
    content += '                        ' + getTime()
    return content


def autoModel(autoMsg, weather, forecast, warning):
    content = ''
    content += '[智能提示]' + autoMsg + '\n\n'
    content += '[地点]' + weather.province + " " + weather.county + '\n'
    content += '------ 当前情况 ------\n'
    content += '[温度] ' + str(weather.temperature) + "℃\n"
    content += "[Pm2.5]" + weather.pm25 + "\n"
    content += "[天气] " + weather.weather_condition + "\n"
    content += "[湿度] " + weather.humidity + '\n'
    content += "[风向] " + weather.wind_direction + '\n'

    if len(warning) > 0:
        content += '------ 现悬挂预警信号 -----\n'
        windex = 0
        while windex < len(warning):
            content += warning[windex].warnTitle + '\n'
            content += '[悬挂时间]' + warning[windex].warnDate + '\n'
            content += '[预警内容]' + warning[windex].warnContent + '\n'
            content += '[预警解析]' + warning[windex].warnAnalysis + '\n'
            content += '[预警提示]' + warning[windex].warnTips + '\n\n'
            windex += 1
    content += '\n\nPS:为什么会收到该邮件?当温差距离上次提醒超过5℃或天气转变或预警信号有变化,即会发送通知提醒!'
    content += '\n\n'
    content += '                        FROM X.M Tips Server\n'
    content += '                        ' + getTime()
    return content
