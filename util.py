#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import configparser
import pymysql
from globalvar import *
from function import *
import urllib.request
import http.cookiejar
import os
import requests
import datetime

def getConf():
    confFile = "conf.ini";
    conf = configparser.ConfigParser();
    conf.read( confFile );
    return conf;

def connectMysql():
    conf = getConf();
    db_host = conf.get('db', 'db_host');
    db_port = conf.getint('db', 'db_port');
    db_user = conf.get('db', 'db_user');
    db_pass = conf.get('db', 'db_pass');
    db_name = conf.get('db', 'db_name');
    db_prefix = conf.get('db', 'db_prefix');
    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pass,db=db_name, charset='utf8');
    cursor = conn.cursor();
    set_value("conn",conn);
    set_value("mysql",cursor);
    # return cursor;

def setConf( cookies_file ):
    set_value( "conf", cookies_file );

def initUrllib():
    # TODO
    cookieFile = "cookies.txt";
    cookies_file = get_value("conf");
    cookie = http.cookiejar.LWPCookieJar();
    if os.path.exists( cookieFile ):
        cookie.load( cookieFile, ignore_discard=True, ignore_expires=True);
    handler = urllib.request.HTTPCookieProcessor(cookie);
    opener = urllib.request.build_opener(handler);
    urllib.request.install_opener(opener);
    set_value("urllib",urllib);

# origin,为True时返回对象，否则返回文本
def requestsGET( url, headers={}, origin=None ):
    res = requests.get( url, headers=headers );
    res.encoding = 'utf-8'
    if origin:
        return res;
    else:
        return res.text;

def getDbPrefix():
    conf = getConf();
    db_prefix = conf.get('db', 'db_prefix');
    return db_prefix;

def commitDB( sql ):
    db = get_value("conn");
    mysql = get_value("mysql");
    mysql.execute(sql)
    db.commit()

def getDateTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');