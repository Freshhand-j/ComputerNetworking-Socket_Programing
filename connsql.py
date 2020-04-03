#!/usr/bin/env python
# -*- coding=utf-8 -*-


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

# 上传新文件 val = (文件名，文件大小，目标路径，权限，上传者)


def dbFileInsert(val):
    mycursor.execute(
        "INSERT INTO file (filename, filesize, filepath, priviledge, uploader) \
        VALUES ('%s', '%s', '%s', '%s', '%s')" % val)

    # 数据更新 要用到下面语句：
    mydb.commit()

# 删除已上传的文件 val = (文件路径)


def dbFileRemove(val):
    try:
        mycursor.execute(
            "SELECT count(*) FROM file WHERE filepath = '%s'" % val)
        affected = mycursor.fetchone()[0]
        mycursor.execute(
            "DELETE FROM file WHERE filepath = '%s'" % val)
        print (affected)
        if affected:
            info = "OK."
            mydb.commit()
        else:
            info = 'No change.'
    except:
        info = 'ERROR!'
    return info

# 显示当前用户可下载的所有文件 val = 当前用户


def dbFileReviewByLocal(val):
    mycursor.execute(
        "SELECT * FROM file WHERE priviledge = '%s' OR priviledge =  'all'" % val)
    myresult = mycursor.fetchall()  # 获取全部记录
    for i in myresult:
        print(i)

#5 显示某用户上传的所有文件 val = 上传用户


def dbFileReviewByUploader(val):
    mycursor.execute(
        "SELECT * FROM file WHERE uploader = '%s'" % val)
    myresult = mycursor.fetchall()  # 获取全部记录
    return myresult


# 判断是否存在 val = (文件名，当前用户)


def dbFileExists(val):
    mycursor.execute("SELECT * FROM file WHERE filename = '%s' \
        AND (priviledge = '%s' OR priviledge = 'all')" % val)
    myresult = mycursor.fetchall()
    for i in myresult:
        print("fileID: {0} ,filepath: {1}, uploader: {2}.".format(
            i[0], i[3], i[5]))

# 查找文件名带有某一字段的文件 val = (文件名字段)

##⭐⭐foemat有问题
def dbFileSearch(val):
    mycursor.execute("SELECT * FROM file WHERE filename LIKE '%{0}%'".format(val))
    myresult = mycursor.fetchall()
    return myresult


#4  查找当前用户存储的所有文件
def db_File_Review_Present(val):
    mycursor.execute("SELECT * FROM file WHERE priviledge = '%s' OR priviledge =  'all'" % val)
    myresult = mycursor.fetchall()
    return myresult

#6 删除 文件
def db_delete_file(val):
    try:
        mycursor.execute("delete from file where filename = '%s'" % val)
        info = 'OK!'
    except:
        info = 'ERROR!'
    return info


# ------------------------------------------用户--------------------------

# 注册新用户 val = (用户名，密码)
def dbUserInsert(val):
    mycursor.execute(
        "INSERT INTO user (username, passwd) VALUES ('%s', '%s')" % val)
    mydb.commit()

# 判断用户是否存在，不存在返回0 val = 用户名


def dbUserExists(val):
    mycursor.execute("SELECT count(*) FROM user WHERE username = '%s'" % val)
    stat = mycursor.fetchone()
    print("dbUserExists: " + str(stat[0]))
    return stat[0]

# 判断用户密码是否正确，不正确返回0 val = (用户名，密码)


def dbUserCheckPwd(val):
    mycursor.execute(
        "SELECT count(*) FROM user WHERE username = '%s' AND passwd = '%s'" % val)
    stat = mycursor.fetchone()
    print("dbUserCheckPwd: " + str(stat[0]))
    return stat[0]
