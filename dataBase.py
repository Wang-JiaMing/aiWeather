#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql


# --查询
def getDataforOne(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='weather',charset="utf8")
    cur = conn.cursor()
    cur.execute(sql)  # "SELECT count(1) FROM weather"
    data=''
    for r in cur.fetchall():
        data=r[0]
    return data
    conn.close()


# --插入
def insertManySql(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='weather',charset="utf8")
    cur = conn.cursor()
    try:
        index=0
        while index < len(sql) :
            print(sql[index])
            cur.execute(sql[index])
            print("插入成功")
            index += 1
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
