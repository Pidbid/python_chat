# -*- encoding: utf-8 -*-
'''
@File    :   monitor.py
@Time    :   2021/11/14 23:13:31
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from threading import Thread
from modules import variable
import time,json

class MONITOR(Thread):
    """
    新建一个线程，循环将消息池的消息发给用户
    """
    def __init__(self):
        super(MONITOR,self).__init__()
        
    def user_online(self):
        if int(time.time())%5 == 0:
            online_users = [{"username":i["name"],"avatar":i["avatar"]} for i in variable.CHAT_USERS]
            if variable.WEBSOCKET != None:
                variable.WEBSOCKET.send_message_to_all(json.dumps({"status":"online","users":online_users}))
    
    def thread_fun(self):
        while True:
            #print("在线用户为",variable.CHAT_USERS)
            # for user in variable.CHAT_USERS:
            #     variable.WEBSOCKET.send_message(user["client"],json.dumps({"status":"online","users":self.user_online()}))
            #self.user_online()
            #print("all message{}".format(variable.CHAT_MESSAGES))
            for msg in variable.CHAT_MESSAGES:
                for user in variable.CHAT_USERS:
                    if msg["to"] == user["name"]:
                        variable.WEBSOCKET.send_message(user["client"],json.dumps(msg))
                        if msg in variable.CHAT_MESSAGES:
                            variable.CHAT_MESSAGES.remove(msg)
            time.sleep(0.5)
        
    def run(self):
        self.thread_fun()
    
