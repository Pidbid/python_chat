# -*- encoding: utf-8 -*-
'''
@File    :   client.py
@Time    :   2021/11/06 22:30:38
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
import asyncio
from websockets import connect

async def hello(uri):
    async with connect(uri) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello("ws://localhost:4456"))