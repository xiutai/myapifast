import pymysql
import time
db = ""
cur = ""
# 现在年月日
try:
  # 数据库配置
  config = {
    "host": "103.124.104.150", 
    "port": 3306, 
    "user": "root", 
    "password": "dasini123", 
    "db": 'dy', 
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
  }
  db = pymysql.connect(**config)
  # 游标
  cur = db.cursor()
except:
  print("连接数据库失败")
  exit(-1)

#查询数据
def res_data(sql):
  try:
    cur.execute(sql)
    return cur.fetchall()
  except Exception as e:
    return e

#执行sql语句
def update(sql,username=''):
  try:
    cur.execute(sql)
    return db.commit()
  except Exception as e:
    return e

#插入数据
def insert(data):
  try:
    sql="insert into `user`(`user`,`pwd`,`comefrom`,`status`,`time`) values('%s','%s','%s',%d,'%s')"%(data.user,data.pwd,data.comefrom,0,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    cur.execute(sql)
    db.commit()
    qf="select max(id) as user_id from user where user='%s'"%(data.user)
    cur.execute(qf)
    return cur.fetchall()
  except Exception as e:
    return e


#查询数据
def cx_data(sql):
  try:
    cur.execute(sql)
    # s=cur.fetchone()
    # db.close()
    return cur.fetchall()
  except Exception as e:
    return e