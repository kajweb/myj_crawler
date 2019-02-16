#!/usr/bin/python
# -*- coding: UTF-8 -*- 

from function import *
from globalvar import *
from util import *
import json

# 初始化全局变量
globalvar_init();
# 初始化mysql库
connectMysql();
#初始化Urllib
# curl = initUrllib();

# 请补充
authorization = "";

categoryResponse = getCategory(authorization);
categoryData = json.loads( categoryResponse );
parseCategory( categoryData['data'] );

mysql = get_value("mysql");
mysql.execute("select * from myj_category where deal = 0");
data = mysql.fetchall()
for i in data:
	id = i[0];
	name = i[1];
	title = i[2];
	#datetime = i[4];
	# getBook( id, name, title )
	getBook( id, authorization );