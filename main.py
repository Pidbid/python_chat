# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/11/14 18:39:12
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from threading import Thread
from fastapi import FastAPI, Cookie,WebSocket,WebSocketDisconnect
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from modules import security, server,monitor
from typing import List
import json
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"],
)  # 允许跨域的headers，可以用来鉴别来源等作用。
# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
# 模板文件夹
templates = Jinja2Templates(directory="templates")
#公共函数
            
# 函数初始化
SECURITY = security.SECURITY(10080,"HELLOWORLD")
MONITOR = monitor.MONITOR()
SERVER = server.SERVER()

# 页面
@app.get("/")
async def page_index(request:Request,token:str = Cookie(None)):
    auth_result = SECURITY.token_auth(token=token)
    if auth_result["code"] == 0:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(url="/login")
    
@app.get("/login")
async def page_login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

# API
@app.get("/api/login")
async def api_login(username:str,password:str):
    return SECURITY.token_creat(username=username,password=password)

@app.get("/api/token_auth")
async def api_tokenauth(token:str):
    return SECURITY.token_auth(token=token)

@app.get("/api/userinfo")
async def api_userinfo(token):
    token_result = SECURITY.token_auth(token=token)
    userinfo = {}
    if token_result["code"] == 0:
        with open("data/users.json") as fp:
            for user in json.loads(fp.read())["users"]:
                if user["username"] == token_result["result"]["username"]:
                    userinfo = user
                    del userinfo["password"]
    if "username" in userinfo.keys():
        return {"code":0,"data":userinfo}
    else:
        return {"code0":0,"data":"wrong token"}
    
#websocket
        
if __name__ == "__main__":
    import uvicorn
    # 多线程启动
    SERVER.start()
    MONITOR.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8888, log_level="info", reload=True)
    