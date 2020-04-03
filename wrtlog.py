#!/usr/bin/env python
# -*- coding=utf-8 -*-


import time
f = None
LOGFILEPATH = '/root/log'


def setfilepath(path):
    global LOGFILEPATH
    LOGFILEPATH = path


def login(username):
    timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    global f
    f = open('{0}/user.log'.format(LOGFILEPATH), "a+")
    f.write("-"*60 + '\n\n')
    f.write("New connection...\n")
    f.write("Current User: " + str(username) + "\tCurrent Time: "+timestr+'\n')
    f.write("-"*60 + '\n')
    f.write('Time'.center(20, ' ') + '|Flag|' +
            'Filepath'.center(23, ' ')+'| Filesize \n')
    f.write('-'*20+'+----+'+'-'*23+'+----------\n')


def wrtlog(flag, filepath='', filesize=0):
    timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spacestr = ''
    if len(timestr) < 20:
        spacestr = ' '*(20-len(timestr))
    timestr = str(spacestr)+str(timestr)

    pathstr = " "*23
    if len(filepath) > 23:
        pathstr = str(filepath)[:20]+'...'
    else:
        pathstr = str(filepath).center(23, ' ')
    sizestr = str(filesize).center(10, ' ')

    f.write('{0}|  {1} |{2}|{3}\n'.format(
        timestr, str(flag), pathstr, sizestr))
    f.write('-'*20+'+----+'+'-'*23+'+----------\n')


def logout(username):
    timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spacestr = ''
    if len(timestr) < 20:
        spacestr = ' '*(20-len(timestr))
    timestr = str(spacestr)+str(timestr)
    f.write(timestr+"| USER {0} LOGOUT.\n".format(username))
    f.close()

'''
TEST

if __name__ == '__main__':
    setfilepath("d:/")
    print(LOGFILEPATH)
    login("zpr")
    wrtlog(1, "/root/data/pi.lllp", 89731)
    wrtlog(2, "D:/Study/socket/sourcfdfkdfdjfkd/", 898989898)
    logout("zpr")
'''