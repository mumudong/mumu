# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import codecs
import sys
import csv
reload(sys)

sys.setdefaultencoding('utf8')
# f = codecs.open("/export/text.txt", "w", encoding="utf-8")
csvFile = codecs.open( '/export/baseCompare.csv', 'w',encoding="utf-8")
column_csvFile = codecs.open( '/export/columnCompare.csv', 'w',encoding="gbk")
base_dict_head = ['jobName','accessUser' ]
base_dict = {}
column_dict_head = ['jobName','field_name']
column_dic = {}
baseWriter = csv.DictWriter(csvFile,base_dict_head,extrasaction='ignore')
baseWriter.writeheader()
columnWriter = csv.DictWriter(column_csvFile,column_dict_head,extrasaction='ignore')
columnWriter.writeheader()
config = {
    "host":"xx",
    "user":"xx",
    "password":"xx",
    "database":"xx",
    "charset":"utf8"

}
conn = pymysql.connect(**config)
cursor = conn.cursor()

def dict_fetchall(cursor,sql):
    "Return all rows from a cursor as a dict"
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getRows(cursor,sql,i):
    cursor.execute(sql)
    result = []    
    for row in cursor.fetchall():
        result.append(row[i])
    return result

def merge_dict(dict1, dict2):
    if dict1 is None:
        return dict2
    if dict2 is None:
        return dict1
    for k,v in dict1.items():
        if dict1[k] is not None:
            dict2[k] = v
    return dict2

try:
    for db in dbs:
        print("id:{},域名:{} ==================================================>".format(db[0],db[1]))
        dbId = db[0]
        getStageJobSql = """ 
            select  
             where c.database_id = {database_id}
               and d.enable != 2
               and a.etl_job like 'S$_%' ESCAPE '$'
        """.format(database_id = dbId)
        cursor.execute(getStageJobSql)
        stageJobs = cursor.fetchall()
        for stageJob in stageJobs:
            findDiff(stageJob[0],stageJob[1],db[3])
finally:
    conn.close()
    # f.close()
    csvFile.close()
    column_csvFile.close() 
