# -*- encoding: utf-8 -*-
"""
@File    :   chat.py
@Time    :   2021/10/23 21:12:03
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
"""


# here put the import lib
from threading import Thread
from queue import Queue
import asyncio
from websockets import serve
import json


class CHAT():
    def __init__(self):
        super(CHAT, self).__init__()
        self.daemon = True
        self.USER = set()
        self.MESSAGE = []

    def login(self,uid):
        self.USER.add(uid)

    def logout(self, ws,uid):
        if uid in self.USER:
            self.USER.remove(uid)
        else:
            ws.close()
            
    def rec_msg(self,data):
        pass

    def recv_msg(self, ws, recv_data):
        recvmsg = json.loads(recv_data)
        uid = recvmsg["uid"]
        status = recvmsg["status"]
        if status == "login":
            self.login(uid)
        elif status == "logout":
            self.logout(ws,uid)
        else:
            if recvmsg["to"] in self.USER_DICT.values():
                pass

    def send_msg(self, ws, send_data):
        pass

    async def main_fun(self, websocket, path):
        async for message in websocket:
            await websocket.send(message)

    async def main_loop(self):
        async with serve(self.main_fun, "localhost", 4456):
            await asyncio.Future()  # run forever

    def run(self):
        print("start chat server")
        asyncio.run(self.main_loop())

if __name__ == "__main__":
    chat = CHAT()
    chat.run()