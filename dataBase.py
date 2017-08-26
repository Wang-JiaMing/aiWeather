#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import time
import pytz
import datetime


def getTime():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


# --查询
def getDataforOne(sql):
    conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', passwd='root', db='aiWeather', charset="utf8")
    cur = conn.cursor()
    cur.execute(sql)  # "SELECT count(1) FROM weather"
    data = ''
    for r in cur.fetchall():
        data = r[0]
    return data
    conn.close()


def getDataAll(sql):
    conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', passwd='root', db='aiWeather', charset="utf8")
    cur = conn.cursor()
    cur.execute(sql)  # "SELECT count(1) FROM weather"
    return cur.fetchall()
    conn.close()


# --插入
def insertManySql(sql):
    conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', passwd='root', db='aiWeather', charset="utf8")
    cur = conn.cursor()
    try:
        index = 0
        while index < len(sql):
            print(sql[index])
            cur.execute(sql[index])
            print("[" + getTime() + "]插入成功")
            index += 1
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def update(sql):
    conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', passwd='root', db='aiWeather', charset="utf8")
    cur = conn.cursor()
    try:
            cur.execute(sql)
            print("[" + getTime() + "]更新成功")
            conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
