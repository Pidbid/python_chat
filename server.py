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
import json
import time
import logging


class SERVER():
    def __init__(self):
        super(SERVER,self).__init__()
        self.USERS = []
        self.MESSAGE = []
        self.server = WebsocketServer(host="0.0.0.0",port=4456)
        self.server.set_fn_new_client(self.client_connect)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    def therad_fun(self):
        for msg in self.MESSAGE:
            for user in self.USERS:
                if msg["to"] == user["uid"]:
                    self.server.send_message(user["client"],msg["data"])
                    self.MESSAGE.remove(msg)
    
    def thread_main(self):
        while True:
            self.therad_fun()
            time.sleep(0.5)
    
    def client_connect(self,client,server):
        self.USERS.append({"client":client,"id":client["id"]})
    
    # 当旧的客户端离开
    def client_left(self,client, server):
        print("客户端%s断开" % client['id'])
    
    # 接收客户端的信息。
    def message_received(self,client, server, message):
        data = json.loads(message)
        if data["status"] == "login":
            for user in self.USERS:
                if client["id"] == user["id"]:
                    user["uid"] = data["uid"]
        elif data["status"] == "logout":
            for user in self.USERS:
                if client["id"] == user["id"]:
                    self.USERS.remove(user)
        elif data["status"] == "chat":
            self.MESSAGE.append(data)
            
    def run(self):
        Thread(target=self.thread_main).start()
        self.server.run_forever()
        
a = SERVER()
a.run()