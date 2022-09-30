import pymysql
import time
db = ""
cur = ""
# 现在年月日
today = time.strftime("%Y-%m-%d", time.localtime())
try:
  # 数据库配置
  config = {
    "host": "127.0.0.1", 
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
def update(sql):
  try:
    cur.execute(sql)
    db.commit()
    return 'ok'
  except Exception as e:
    return e

# sql="DELETE FROM `user` where id = %d"%(1)
sql="UPDATE `user` SET `status`=%d where id =%d;"%(1,200)
cur.execute(sql)
db.commit()