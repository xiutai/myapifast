import pymysql
import time
db = ""
cur = ""
# 现在年月日
try:
  # 数据库配置
  config = {
    "host": "127.0.0.1", 
    "port": 3306, 
    "user": "root", 
    "password": "root", 
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

#查询一条数据
def cx_data(sql,values):
  try:
    cur.execute(sql,values)
    return cur.fetchone()
  except Exception as e:
    return e

#执行sql语句
def update(sql,values):
  try:
    cur.execute(sql,values)
    return db.commit()
  except Exception as e:
    return e

#插入数据
def insert(sql,data):
  try:
    cur.execute(sql,data)
    db.commit()
    qf="select max(id) as user_id from user where user=%s"
    cur.execute(qf,(data[0]))
    return cur.fetchone()
  except Exception as e:
    return e


