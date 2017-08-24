import mjWeather

from server import sendMail

msg = mjWeather.getWeatherMsg() + '\n\n——来自小明AI管家实时天气情况'
sendMailAddress = ['13422192925@163.com']#,'352294249@qq.com', '601229570@qq.com'
for address in sendMailAddress:
    sendMail.sendMail(mjWeather.getWeatherTitle(), msg, address)
