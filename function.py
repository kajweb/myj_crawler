#!/usr/bin/python
# -*- coding: UTF-8 -*- 

from globalvar import *
from util import *
import json
import math

def getCategory( authorization ):
    headers = { "authorization": authorization }
    url = "https://app.manyoujing.net/v1/book/category/all";
    data = requestsGET( url, headers );
    return data;

def parseCategory( data ):
    for BigCategory in data:
        title = BigCategory['title'];
        for SmallCategory in BigCategory['items']:
            id =  SmallCategory['id'];
            name =  SmallCategory['name'];
            saveCategoryToDB( id, name, title );

def saveCategoryToDB( id, name, title ):
    print( "保存栏目：", id, name, title );
    db_prefix = getDbPrefix();
    db_table = "category";
    datetime = getDateTime();
    sql = "replace into {}{}(`id`,`name`,`title`,`cTime`,`deal`)values('{}','{}','{}','{}','{}')".format( db_prefix, db_table, id, name, title, datetime, 0 );
    commitDB(sql);

def getBook( id, authorization, page=1 ):
    size = 10;
    headers = { "authorization": authorization }
    url = "https://app.manyoujing.net/v1/book/list/{}?page={}&size={}".format( id, page, size );
    book = requestsGET( url, headers );
    bookJson = json.loads( book );
    # 保存数据 TODO优化
    data = bookJson['data']['items'];
    saveBook( data, id );
    # 总条数
    total = bookJson['data']['total'];
    # 计算总页数
    pages = math.ceil(float(total)/size);
    print( "更新书籍状态中", "ID：", id, "页码：", page );
    if page < pages:
        getBook( id, authorization, page+1 );
    else:
        # 修改为已经查询，更新相关数据
        image = bookJson['data']['image'];
        changeCategoryStatus( id, total, image );
        # exit();

def changeCategoryStatus( id, total, image ):
    print( "修改栏目状态：", id, total );
    db_prefix = getDbPrefix();
    db_table = "category";
    datetime = getDateTime();
    sql = "UPDATE {}{} SET `total`='{}',`image`='{}',`update`='{}',`deal`='{}' where id = {}".format( db_prefix, db_table, total, image, datetime, 1, id );
    commitDB(sql);


def saveBook( data, categoryId ):
    for item in data:
        image           = item['image'];
        title           = item['title'];
        author          = item['author'];
        rating_average  = item['rating_average'];
        price           = item['price'];
        product_price   = item['product_price'];
        gid             = item['gid'];
        sub_title       = item['sub_title'];
        category_id     = categoryId;
        datetime        = getDateTime();
        print( "更新书籍：", title, rating_average, gid );
        db_prefix = getDbPrefix();
        db_table = "book";
        datetime = getDateTime();
        sql = "replace into {}{}(`image`,`title`,`author`,`rating_average`,`price`,`product_price`,`gid`,`sub_title`,`category_id`,`cTime`)values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format( db_prefix, db_table, image,title,author,rating_average,price,product_price,gid,sub_title,categoryId,datetime );
        commitDB(sql);