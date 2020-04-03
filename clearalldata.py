#!/usr/bin/env python 
# -*- coding=utf-8 -*-
import os
import mysql.connector
DATABASE_NAME = "socket"
# 数据库连接
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database=DATABASE_NAME
)
# 游标 当前行
mycursor = mydb.cursor()
mycursor.execute("TRUNCATE TABLE file")

mydb.close()

os.popen("rm -rf /root/data/*")