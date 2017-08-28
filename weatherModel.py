# -*- coding:utf-8 -*-
class weatherModel:
    id = ''
    overview = ''
    province = ''
    county = ''
    temperature = ''
    weather_condition = ''
    humidity = ''
    wind_direction = ''
    msg_update_time = ''
    create_date = ''
    pm25 = ''
    warning = ''
    status = ''
    autoTips = ''
    makeup = ''
    cold = ''
    car_wash = ''
    air_pollution = ''
    dress = ''
    ultraviolet_rays = ''
    sport = ''
    go_fishing = ''

    def __init__(self, id, overview, province, county, temperature, weather_condition, humidity, wind_direction,
                 msg_update_time, create_date, pm25, warning, status, autoTips, makeup, cold, car_wash, air_pollution,
                 dress, ultraviolet_rays, sport, go_fishing):
        self.id = id
        self.overview = overview
        self.province = province
        self.county = county
        self.temperature = temperature
        self.weather_condition = weather_condition
        self.humidity = humidity
        self.wind_direction = wind_direction
        self.msg_update_time = msg_update_time
        self.create_date = create_date
        self.pm25 = pm25
        self.warning = warning
        self.status = status
        self.autoTips = autoTips
        self.makeup = makeup
        self.cold = cold
        self.car_wash = car_wash
        self.air_pollution = air_pollution
        self.dress = dress
        self.ultraviolet_rays = ultraviolet_rays
        self.sport = sport
        self.go_fishing = go_fishing
