import smtplib
import time
from email.mime.text import MIMEText


def sendMail(title, mailContent, toMailList):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # SMTP服务器
    mail_user = "519677263@qq.com"  # 用户名
    mail_pass = "13533708697"  # 密码
    sender = '519677263@qq.com'  # 发件人邮箱(最好写全, 不然会失败)
    receivers = toMailList  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    content = mailContent
    title = title  # 邮件主题
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print(time.strftime("["+"%Y-%m-%d %H:%M:%S", time.localtime())+']'+receivers + " 发送成功")
    except smtplib.SMTPException as e:
        print(receivers + "\n" + e)
