#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import division
from time import sleep
from prettytable import PrettyTable
import socket
import os
import sys
import struct
import argparse
import time
import math
import json
# 进度条提示


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' %
                     ('*' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    if cur == total:
        sys.stdout.write('\n')


# 获取用户密码


def get_name_passwd():
    args = parser.parse_args()
    username = args.username
    passwd = args.passwd
    return username, passwd


# 用户验证


def userIdentify(username, password):
    userinfo_size = struct.calcsize('128s128s')
    # 定义文件头信息，包含文件名和文件大小
    uhead = struct.pack(
        '128s128s',
        username.encode('utf-8'),
        password.encode('utf-8')
    )
    s.send(uhead)
    recv_len = struct.calcsize('1s')
    stat = s.recv(recv_len)
    return int(stat)

#主界面
def client():
    # 进行用户验证
    username, passwd = get_name_passwd()
    userStat = userIdentify(username,passwd)
    if userStat == -1:
        print('Username incorrect.')
        s.close()
    elif userStat == -2:
        print('Wrong password!')
        s.close()
    else:
        print('Welcome to the server, {0}!'.format(username))
    while True:
        # 上传下载选择
        print("Enter a number to choose what to do:".center(50, '='))
        print('')
        print("\t1:\t上传")
        print("\t2:\t下载")
        print("\t3:\t查找文件名带有某字段的所有文件")
        print("\t4:\t显示当前用户能下载的所有文件")
        print("\t5:\t显示某用户上传的所有文件")
        print("\t6:\t删除已上传的文件")
        print("\t0:\t退出（默认）")

        num = input("\nEnter your choose:")
        while 1:
            if num == '':
                break
            elif str(num).isdigit == False:
                pass
            else:
                if int(num)>=0 and int(num)<=6:
                    break
            print("无效输入")
            num = input("Enter your choose:")
        print("="*50)

        #s.send(str(num)

        if num == '1':
            flag = 1
            upload(flag)
        elif num == '2':
            flag = 2
            download(flag)
        elif num == '3':
            flag = 3
            searchas(flag)
        elif num == '4':
            flag = 4
            coulddownload(flag)
        elif num == '5':
            flag = 5
            uploadedfiles(flag)
        elif num == '6':
            flag = 6
            delet_file(flag)
        else:
            flag = 0
            s.send(pack_operatrion(flag))
            print('Exit.')
            break
        print("")
    s.close()

#1 测试成功
def upload(flag):
    filepath = input('Enter filepath:\n')
    destination_path = input('Enter destination path:\n')
    destination = destination_path
    print(filepath)
    arg = ''
    if os.path.isfile(filepath):

        #打包
        operatrion = pack_operatrion(flag,arg,filepath,destination)

        print(os.path.basename(filepath))

        print('client filepath: {0}'.format(filepath))
        s.send(operatrion)

        # 上传数据
        fp = open(filepath, 'rb')
        sent_size = 0
        totalsize = os.stat(filepath).st_size
        while 1:
            data = fp.read(1024)
            sent_size += len(data)
            progressbar(sent_size*100/totalsize, 100)
            if not data:
                print('\r{0} file send over...'.format(filepath))
                break
            s.send(data)
    #报错 连接关闭过早
    #File "/usr/lib/python2.7/socket.py", line 174, in _dummy
    #raise error(EBADF, 'Bad file descriptor')
    #error: [Errno 9] Bad file descriptor
    #s.close()

#2 测试成功
def download(flag):
    #发送请求
    arg = ''
    #⭐计算效率⭐
    start = time.time()
    filepath = input('输入源文件路径:\n')
    destination = input('下载到本机地址:\n')

    # print(filepath)
    opreation = pack_operatrion(flag,arg=filepath,destination=destination)

    print('Server filepath: {0}'.format(filepath))
    s.send(opreation)

    # ---------------------------接收 要下载的文件头部信息---------------------------
    receive_infosize = struct.calcsize('i128si128s')

    # 接受缓冲池中服务器发来的问候，清空缓冲池
    buf = s.recv(receive_infosize)
    # print(buf)

    if buf:
        flag, filepath, filesize, destination = struct.unpack(
            'i128si128s', buf)

        # 解析文件路径
        # print(flag+'\n'+filepath+'\n'+filesize+'\n'+destination)
        fn = destination.decode('utf-8').strip('\00')
        filename = os.path.basename(filepath.decode('utf-8'))
        filepath = (fn + filename).encode('utf-8')
        filepath = filepath.decode('utf-8').strip('\00')

        # 接收文件
        recvd_size = 0
        fp = open(filepath, 'wb+')
        print('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = s.recv(1024)
                recvd_size += len(data)
                progressbar(recvd_size*100/filesize, 100)
            else:
                data = s.recv(filesize - recvd_size)
                recvd_size = filesize
                progressbar(100, 100)
            fp.write(data)
        fp.close()
        end = time.time()
        #⭐⭐
        print(end-start)
        print('end receive...')
    #报错
    #s.close()

#3 建议删除
def searchas(flag):
    arg = input('Enter the *FILENAME*:')
    operation = pack_operatrion(flag, arg=arg)
    s.send(operation)
    #返回结果小于1024B
    buf = s.recv(1024)
    feedback_list = json.loads(buf)
    feedback_table = PrettyTable(["id","filename","filesize","filepath","priviledge","uploader"])
    for i in feedback_list:
        feedback_table.add_row(i)
    print(feedback_table)
    sleep(1)

#4 测试成功
def coulddownload(flag):
    arg = ''
    filepath = os.path.abspath(__file__)
    destination = ''
    operation = pack_operatrion(flag,arg,filepath,destination)
    s.send(operation)
    #返回结果小于1024B
    buf = s.recv(1024)
    feedback_list = json.loads(buf)
    feedback_table = PrettyTable(["id","filename","filesize","filepath","priviledge","uploader"])
    for i in feedback_list:
        feedback_table.add_row(i)
    print(feedback_table)
    sleep(1)

#5 测试成功
def uploadedfiles(flag):
    arg = input('Enter the *USERNAME*:')
    operation = pack_operatrion(flag, arg=arg)
    s.send(operation)
    #print('send!')
    #返回结果小于1024B
    buf = s.recv(1024)
    feedback_list = json.loads(buf)
    feedback_table = PrettyTable(["id","filename","filesize","filepath","priviledge","uploader"])
    for i in feedback_list:
        feedback_table.add_row(i)
    print(feedback_table)
    sleep(1)

#6 测试成功
def delet_file(flag):
    filepath = os.path.abspath(__file__)
    destination = ''
    arg = input('Enter the *FILEPATH* you want to delete:\n')
    operation = pack_operatrion(flag,arg,filepath,destination)
    s.send(operation)
    feedback = s.recv(1024)
    print(feedback.decode ('utf-8'))
    sleep(1)

#数据功能 统一打包方式
def pack_operatrion(flag,arg='',filepath=os.path.abspath(__file__),destination=''):
    #sql_size = struct.calcsize('i128s128si128s')
    filesize = os.stat(filepath).st_size
    operation = struct.pack(
        'i128s128si128s',
        flag,
        arg.encode('utf-8'),
        os.path.basename(filepath).encode(encoding="utf-8"),
        filesize,
        destination.encode('utf-8')
    )
    return operation


if __name__ == "__main__":

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 测试 虚拟机地址
        #s.connect(('192.168.127.128', 16421))
        # 服务器地址
        s.connect(('123.56.115.192', 10086))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    # hello
    print(s.recv(1024).decode('utf-8'))

    parser = argparse.ArgumentParser(description='Login')

    parser.add_argument('-u', '--user', action='store',
                        type=str, dest='username', required=True, help='用户名')
    parser.add_argument('-p', '--passwd', action='store',
                        type=str, dest='passwd', required=True, help='目标目录')
    client()
