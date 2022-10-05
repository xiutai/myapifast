from fastapi import FastAPI, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
import pymysql
import mysql
import hash
import time

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
    sql="select * from admin where username=%s"
    return mysql.cx_data(sql,(username))

#表单登录
@app.post("/admin/login_form", response_model=hash.Token)
async def login_for_access_token(form_data: hash.OAuth2PasswordRequestForm = hash.Depends()):
    hash.oauth2_scheme=hash.OAuth2PasswordBearer(tokenUrl="/admin/login_form")
    print(hash.fake_users_db)
    user = hash.authenticate_user(test(form_data.username), form_data.username, form_data.password)
    print(user)
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
    user = hash.authenticate_user(test(data.username), data.username, data.password)
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
def admin_rpwd(data:Adminrpwd,current_user: hash.User = hash.Depends(hash.get_current_user)):
    n_pwd=hash.get_password_hash(data.pwd)
    sql="UPDATE `admin` SET `hashed_password`=%s where id =%s;"
    mysql.update(sql,(n_pwd,data.id))
    return 'ok'


#获取用户数据
@app.get("/user")
async def login(current_user: hash.User = hash.Depends(hash.get_current_user)):
    sql='select * from user id ORDER BY id DESC;'
    return mysql.res_data(sql)


#修改状态
class Userstatus(BaseModel):
    id: int
    status: str
@app.post("/user/update")
def user_update(data:Userstatus):
    sql="UPDATE `user` SET `status`=%s where id =%s;"
    mysql.update(sql,(data.status,data.id))
    return 'ok'

#删除用户
class Userid(BaseModel):
    id: int
@app.post("/user/delete")
def user_delete(id:Userid, current_user: hash.User = hash.Depends(hash.get_current_user)):
    sql="DELETE FROM `user` where id = %s"
    mysql.update(sql,(id.id))
    return 'ok'

#修改验证码
class Usercap(BaseModel):
    id: int
    cap: str
@app.post("/user/cap")
def user_cap(data:Usercap):
    sql="update user set cap=%s where id=%s"
    mysql.update(sql,(data.cap,data.id))
    return 'ok'

class User(BaseModel):
    user: str
    pwd: str
    cap: Union[str, None] = None
    comefrom: str
    status:str
#新增用户
@app.post("/user/insert")
def user_insert(data:User):
    sql="insert into `user`(`user`,`pwd`,`comefrom`,`status`,`time`) values(%s,%s,%s,%s,%s)"
    data=(data.user,data.pwd,data.comefrom,'0',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print(data)
    return mysql.insert(sql,data)

#查询状态
@app.post("/user/status")
def user_status(data:Userid):
    sql="select status as zt from user where id=%s"
    return mysql.cx_data(sql,(data.id))
            