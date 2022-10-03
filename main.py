from fastapi import FastAPI, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
import pymysql
import mysql
import hash

app = FastAPI()
# app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)

fsql="'"




class From_data(BaseModel):
    username:str
    password:str






def test(username):
    # username=username.replace("'","")
    sql="select * from admin where username='%s'"%username
    s=mysql.res_data(sql)
    s[0]["disabled"]=False
    ok={}
    ok[s[0]['username']]=s[0]
    return ok

#表单登录
@app.post("/admin/login_form", response_model=hash.Token)
async def login_for_access_token(form_data: hash.OAuth2PasswordRequestForm = hash.Depends()):
    hash.oauth2_scheme=hash.OAuth2PasswordBearer(tokenUrl="/admin/login_form")
    if "'" in form_data.username:
        return
    if "'" in form_data.password:
        return
    hash.fake_users_db=test(form_data.username)
    user = hash.authenticate_user(test(form_data.username), form_data.username, form_data.password)
    if not user:
        raise hash.HTTPException(
            status_code=hash.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = hash.timedelta(minutes=hash.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = hash.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#json登录
@app.post("/admin/login")
async def login_for_access_token(data:From_data):
    hash.oauth2_scheme=hash.OAuth2PasswordBearer(tokenUrl="/admin/login")
    form_data =hash.OAuth2PasswordRequestForm = hash.Depends()
    form_data.username=data.username
    form_data.password=data.password
    if "'" in form_data.username:
        raise HTTPException(status_code=400, detail="nothing")
    if "'" in form_data.password:
        raise HTTPException(status_code=400, detail="nothing")
    hash.fake_users_db=test(form_data.username)
    user = hash.authenticate_user(test(form_data.username), form_data.username, form_data.password)
    if not user:
        raise hash.HTTPException(
            status_code=hash.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = hash.timedelta(minutes=hash.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = hash.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#管理员修改密码
class Adminrpwd(BaseModel):
    id: int
    pwd: str
@app.post("/admin/rpwd")
def admin_rpwd(data:Adminrpwd,current_user: hash.User = hash.Depends(hash.get_current_active_user)):
    n_pwd=hash.get_password_hash(data.pwd)
    sql="UPDATE `admin` SET `hashed_password`='%s' where id =%s;"%(n_pwd,data.id)
    mysql.update(sql)
    return 'ok'


#获取用户数据
@app.get("/user")
async def login(current_user: hash.User = hash.Depends(hash.get_current_active_user)):
    sql='select * from user id ORDER BY id DESC;'
    return mysql.res_data(sql)


#修改状态
class Userstatus(BaseModel):
    id: int
    status: int
@app.post("/user/update")
def user_update(data:Userstatus):
    sql="UPDATE `user` SET `status`=%s where id =%s;"%(data.status,data.id)
    mysql.update(sql)
    return 'ok'

#删除用户
class Userid(BaseModel):
    id: int
@app.post("/user/delete")
def user_delete(id:Userid, current_user: hash.User = hash.Depends(hash.get_current_active_user)):
    sql="DELETE FROM `user` where id = %s"%(id.id)
    mysql.update(sql)
    return 'ok'

#修改验证码
class Usercap(BaseModel):
    id: int
    cap: str
@app.post("/user/cap")
def user_cap(data:Usercap):
    if fsql in data.cap:
        raise HTTPException(status_code=400, detail="nothing")
    sql="update user set cap='%s' where id=%s"%(data.cap,data.id)
    return mysql.update(sql)

class User(BaseModel):
    user: str
    pwd: str
    cap: Union[str, None] = None
    comefrom: str
    status:str
#新增用户
@app.post("/user/insert")
def user_insert(data:User):
    if fsql in data.user or fsql in data.pwd or fsql in data.comefrom or fsql in data.status:
            raise HTTPException(status_code=200, detail="nothing")
    return mysql.insert(data)[0]

#查询状态
@app.post("/user/status")
def user_status(data:Userid):
    sql="select status as zt from user where id=%s"%(data.id)
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
        cur.execute(sql)
        return cur.fetchall()[0]
    except:
        print("连接数据库失败")
        exit(-1)
            