# -*- encoding: utf-8 -*-
'''
@File    :   server.py
@Time    :   2021/11/08 22:08:30
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from websocket_server import WebsocketServer
from threading import Thread
import json,time
from modules import variable


class SERVER(Thread):
    def __init__(self):
        super(SERVER,self).__init__()
        variable.WEBSOCKET = WebsocketServer(host="0.0.0.0",port=8889)
        variable.WEBSOCKET.set_fn_new_client(self.client_connect)
        variable.WEBSOCKET.set_fn_client_left(self.client_left)
        variable.WEBSOCKET.set_fn_message_received(self.message_received)
    
    def client_connect(self,client,server):
        variable.CHAT_USERS.append({"client":client,"id":client["id"],"name":"","avatar":""})
    # 当旧的客户端离开
    def client_left(self,client, server):
        print("客户端%s断开" % client['id'])
        for user in variable.CHAT_USERS:
            if client == user["client"]:
                variable.CHAT_USERS.remove(user)
    
    # 接收客户端的信息。
    def message_received(self,client, server, message):
        data = json.loads(message)
        print("收到：{}，从{} client".format(data,client["id"]))
        if data["status"] == "login":
            for user in variable.CHAT_USERS:
                if client == user["client"]:
                    user["name"] = data["name"]
                    user["avatar"] = data["avatar"]
            online_users = [{"username":i["name"],"avatar":i["avatar"]} for i in variable.CHAT_USERS]
            if variable.WEBSOCKET != None:
                variable.WEBSOCKET.send_message_to_all(json.dumps({"status":"online","users":online_users}))
        elif data["status"] == "logout":
            for user in variable.CHAT_USERS:
                if client["id"] == user["id"]:
                    variable.CHAT_USERS.remove(user)
        elif data["status"] == "chat":
            variable.CHAT_MESSAGES.append(data)
            
    def run(self):
        variable.WEBSOCKET.run_forever()
        