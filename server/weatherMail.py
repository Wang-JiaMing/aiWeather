import weatherHtml
from server import mail
import pojo.weatherModel
import pojo.weatherWarning
import pojo.weatherforecast
from server import dataBase


def getNewMailId():
    sql = 'select id from weather  where status="1"'
    return dataBase.getDataforOne(sql)


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
        wm.weatherModel.makeup = row[14]
        wm.weatherModel.cold = row[15]
        wm.weatherModel.car_wash = row[16]
        wm.weatherModel.air_pollution = row[17]
        wm.weatherModel.dress = row[18]
        wm.weatherModel.ultraviolet_rays = row[19]
        wm.weatherModel.sport = row[20]
        wm.weatherModel.go_fishing = row[21]
    return wm


def getNewForecast(id):
    sql = 'select * from weatherforecast wf where wf.wId="' + id + '" order by f_index asc'
    wflist = []
    for row in dataBase.getDataAll(sql):
        wf = pojo.weatherforecast
        wf.weatherforecast.f_index = row[2]
        wf.weatherforecast.f_time = row[3]
        wf.weatherforecast.situation = row[4]
        wf.weatherforecast.temperature = row[5]
        wf.weatherforecast.wind_direction = row[6]
        wflist(len(wflist), wf)
    return wflist


def getNewWarning(id):
    sql = 'select * from weatherwarning wf where wf.wId="' + id + '"'
    wwlist = []
    for row in dataBase.getDataAll(sql):
        ww = pojo.weatherWarning
        ww.weatherWarning.warnTitle = row[2]
        ww.weatherWarning.warnDate = row[3]
        ww.weatherWarning.warnCountent = row[4]
        ww.weatherWarning.warnAnalysis = row[5]
        ww.weatherWarning.warnTips = row[5]
        wwlist.insert(len(wwlist), ww)
    return wwlist


def main():
    weatherOid = getNewMailId()
    content = ''
    if len(weatherOid) > 0:
        print("xxx")
    else:
        weather = getNewWeatherMsg()
        content += '今天总体情况：' + weather.weatherModel.overview + '\n\n'
        content += '地点：' + weather.weatherModel.province + " " + weather.weatherModel.county + '\n\n'
        content += '------当前情况------\n'
        content += '温度 ' + str(weather.weatherModel.temperature) + "\n"
        content += "Pm2.5 " + weather.weatherModel.pm25 + "\n"
        content += "天气 " + weather.weatherModel.weather_condition + "℃\n"
        content += weather.weatherModel.humidity + '\n'
        content += "风向 " + weather.weatherModel.wind_direction + '\n\n'
        content += '------未来3天预测------\n'
        forecast = getNewForecast(weather.weatherModel.id)
        findex = 0
        while findex < len(forecast):
            content += str(forecast[findex].weatherforecast.f_index) + ". [" + forecast[
                findex].weatherforecast.f_time + "] 天气状况:" + forecast[findex].weatherforecast.situation + " 最低/最高温度:" + \
                       forecast[findex].weatherforecast.temperature + " 风向:" + forecast[
                           findex].weatherforecast.wind_direction
            findex += 1
        print(content)


main()
