# coding=utf-8
import pandas as pd
import sys
import numpy as np
import os
import pymysql

class MySQLClass(object):
    def __init__(self,host,port,user,passwd,db,table):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db
        self.table = table

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.password,db=self.db,charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def queryMysql(self):
        sql = "SELECT * FROM " + self.table

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchall()
            print(row)

        except:
            print(sql + ' execute failed.')

    def insertMysql(self,dictVal):
        ip = dictVal.get('ip',None)
        prefix =dictVal.get('prefix',0)
        asNumber = dictVal.get('asNumber',None)
        asName = dictVal.get('asName',None)
        asOrg = dictVal.get('asOrg',None)
        usage = dictVal.get('usage',None)
        field=""
        value=""
        for key in dictVal.keys():
            if dictVal[key]!=None:
                field+='`'+key+"`"+","
                value+="'"+str(dictVal[key])+"',"
        field=field[:-1]
        value=value[:-1]
        sql = "INSERT INTO " + self.table +"("+field +")"+" VALUES(" +value+ ");"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("数据插入成功:"+sql)
        except:
            print("insert failed.")

    def updateMysqlSN(self,name,sex):
        sql = "UPDATE " + self.table + " SET sex='" + sex + "'" + " WHERE name='" + name + "'"
        print("update sn:" + sql)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()


    def closeMysql(self):
        self.cursor.close()
        self.conn.close()


#获取文件夹下面的全部文件
filenames=os.listdir('data')

#数据库
sql=MySQLClass(host="127.0.0.1",port=3306,user="root",passwd="123456",db="networkip",table="networkip_tbl")
sql.connectMysql()

for filename in filenames:
    df=pd.read_csv('data/%s'%filename,sep=',',encoding='UTF-8')
    val=df.values
    for i in val:
        li=list(map(str,i))
        ip=li[0].split('/')[0]
        prefix=int(float(li[0].split('/')[1]))
        asNumber=None
        asName=None
        asOrg=None
        usage=None
        if li[1] != "nan":
            try:
                asNumber=int(float(li[1]))
            except:
                print ("出现错误 asNumber：",asNumber)
        if li[2] != "nan":
            asName=li[2]
        if li[3] != ' ':
            asOrg=li[3]
        if li[4] != ' ' or li[4] != "nan":
            usage=li[4]
        print(ip,prefix,asNumber,asName,asOrg,usage)
        dictVal={}
        dictVal['ip']=ip
        dictVal['prefix']=prefix
        dictVal['asNumber']=asNumber
        dictVal['asName']=asName
        dictVal['asOrg']=asOrg
        dictVal['usage']=usage

        sql.insertMysql(dictVal)

print("数据库查询>>>>>>>>>\n")
sql.queryMysql()
sql.closeMysql()