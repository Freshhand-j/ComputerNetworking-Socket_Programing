#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import threading
import time
import sys
import os
import struct
import time
from connsql import *
import wrtlog
import json
# 当前用户
online_username = None

# 身份认证(带返回值，-1用户不存在，-2密码错误，1认证成功)


def userIdentify():
    userinfo_size = struct.calcsize('128s128s')
    uhead = conn.recv(userinfo_size)
    username, password = struct.unpack('128s128s', uhead)
    username = username.strip('\00')
    password = password.strip('\00')
    if (dbUserExists(username)):
        if (dbUserCheckPwd((username, password))):
            identifyMsg = 1  # 'Welcome to the server, {0}!'.format(username)
            online_username = username
        else:
            identifyMsg = -2  # 'Wrong password!'
    else:
        identifyMsg = -1  # 'Username incorrect.'
    conn.send(str(identifyMsg))
    return identifyMsg, online_username


# 第二次握手 检验用户信息
def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    conn.send('Socket connected.')
    userStat, online_username = userIdentify()
    if userStat == 1:
        print("User {0} login at thread-{1}.".format(online_username, threading.current_thread().name))
        wrtlog.setfilepath('/root/log')
        wrtlog.login(online_username)
    else:
        conn.close()

    # 接收用户输入flag
    while 1:
        # 操作解包
        size = struct.calcsize('i128s128si128s')
        buf = conn.recv(size)
        flag, arg, filename, filesize, destination = struct.unpack(
            'i128s128si128s', buf)
        arg = arg.strip('\00').decode('utf-8')
        filename = filename.strip('\00').decode('utf-8')
        destination = destination.strip('\00').decode('utf-8')

        # 预览信息 测试用
        print('flag:'+str(flag)+'\targ:'+arg+'\tfilename:'+filename
              + '\tfilesize:'+str(filesize)+'\tdestination:'+destination)

        if flag == 1:
            receive_file(filename, filesize, destination, online_username)
        elif flag == 2:
            send_file(arg, filesize, destination)  # 这里使用arg传递server端文件路径
        elif flag == 3:
            Preview_part_3(arg)
        elif flag == 4:
            Preview_all_4(online_username)
        elif flag == 5:
            Preview_user_5(arg)
        elif flag == 6:
            delet_file_6(arg)
        elif flag == 0:
            print("User {0} logout from thread-{1}.".format(online_username, threading.current_thread().name))
            break
    wrtlog.logout(online_username)
    conn.close()

# 功能 1 接收


def receive_file(filename, filesize, destination, online_username):
    # 解析文件路径
    start = time.time()
    fn = destination.decode('utf-8').strip('\00')
    filename = os.path.basename(filename.decode('utf-8'))
    filepath = (fn + '/'+filename).encode('utf-8')
    filepath = filepath.decode('utf-8').strip('\00')
    recvd_size = 0  # 定义已接收文件的大小
    fp = open(filepath, 'wb+')
    print(filepath)
    print('start receiving...')
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            data = conn.recv(1024)
            recvd_size += len(data)
        else:
            data = conn.recv(filesize - recvd_size)
            recvd_size = filesize
        fp.write(data)
    fp.close()
    end = time.time()
    print(end-start)
    dbFileInsert((filename, filesize, filepath,
                  online_username, online_username))
    print('end receive...')
    # 输出到log文件
    wrtlog.wrtlog(1, filepath, filesize)


# 功能 2 发送
def send_file(filename, filesize, destination):
    # 通过 time和filesize 计算传输效率 ⭐⭐
    start = time.time()
    if os.path.isfile(filename):
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack(  # flag filename size destination
            'i128si128s',
            0,  # 没有意义
            filename.encode(encoding="utf-8"),
            os.stat(filename).st_size,
            destination.encode(encoding="utf-8")
        )
        print('client filepath: {0}'.format(filename))
        conn.send(fhead)
        # 发送数据
        fp = open(filename, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filename))
                break
            conn.send(data)
    # 输出到log文件
    wrtlog.wrtlog(2, filename, os.stat(filename).st_size)


# 功能 3 显示全部
def Preview_part_3(arg):
    # 输出到log文件
    wrtlog.wrtlog(3)
    result = dbFileSearch(arg)
    print(result)
    result_jason = json.dumps(result)
    conn.send(result_jason)

# 功能 4 显示全部


def Preview_all_4(online_username):
    # 输出到log文件
    wrtlog.wrtlog(4)
    result = db_File_Review_Present(online_username)
    print(result)
    result_jason = json.dumps(result)
    conn.send(result_jason)

# 功能 5 显示用户


def Preview_user_5(arg):
    # 输出到log文件
    wrtlog.wrtlog(5)
    result = dbFileReviewByUploader(arg)
    print(result)
    result_jason = json.dumps(result)
    conn.send(result_jason)

# 功能 6 删除


def delet_file_6(arg):
    # 输出到log文件
    wrtlog.wrtlog(6, arg)
    feedback = dbFileRemove(str(arg))
    print(feedback)
    try:
        os.popen("rm -f %s" % arg)
    except Exception as e:
        print(e)
    conn.send(feedback)

# 输出日志文件


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 关闭程序后，立刻释放端口
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('0.0.0.0', 16421))
        s.bind(('0.0.0.0', 10086))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()
