# -*- encoding: utf-8 -*-
'''
@File    :   security.py
@Time    :   2021/11/14 18:58:49
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import json

class SECURITY:
    def __init__(self,expire_time:int,token_key:str):
        self.token_expire = datetime.utcnow() + timedelta(minutes=expire_time)
        self.user_username = ""
        self.user_password = ""
        self.token_key = token_key
        
    def __user_auth__(self):
        """
        验证用户名和密码是否正确的函数,此处并未使用数据库，使用data目录下的users.json存储用户数据
        """
        with open("data/users.json") as fp:
            self.user_db = json.loads(fp.read())["users"]
        result_user = 0
        for user in self.user_db:
            if self.user_username == user["username"] and self.user_password == user["password"]:
                result_user = 1
            else:
                continue
        if result_user == 1:
            return True
        else:
            return False
    
    def token_creat(self,username:str,password:str):
        """
        生成token的函数
        Args:
            username (str): [用户名]
            password (str): [密码]
        """
        self.user_username = username
        self.user_password = password
        if self.__user_auth__():
            encode_dict = {"exp": self.token_expire, "username":username}
            encoded_jwt = jwt.encode(encode_dict, self.token_key, algorithm="HS256")
            other_msg = {}
            for user in self.user_db:
                if user["username"] == username:
                    other_msg.update({"username":username,"avatar":user["avatar"]})
            return {"code":0,"data":encoded_jwt,"other":other_msg}
        else:
            return {"code":1,"data":"wrong username or password"}

    def token_auth(self,token:str=None):
        """
        验证token的函数
        Args:
            token ([str]): [传入的token]
        """
        if token == None:
            return {"code":1,"data":"token auth failed"}
        self.user_token = token
        try: 
            auth_result = jwt.decode(self.user_token,self.token_key,algorithms="HS256")
            return {"code":0,"data":"login success","result":auth_result}
        except ExpiredSignatureError as e:
            return {"code":1,"data":"token expred"}
        except JWTError as e:
            return {"code":1,"data":"token auth failed"}
