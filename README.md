# python_chat  
一个python实现的聊天框架   
![main image](https://github.com/Pidbid/python_chat/static/image/main.jpg)

最近自己所做的项目需要一个聊天的功能，但是目前可用的有网易的 IM 以及其他公司提供的功能都很好用，但是出于练手的目的，所以重新写了一个简单的聊天功能，相当于制作轮子？

### 采用的技术栈  

Python:

Fastapi 一个写 API 的框架

websocket_server 一个简单的框架，用来搭建 websocket 服务端

jose 用来做 jwt 验证的第三方库

Html+js+css

Cookies 一个第三方 cookies 的 js 库，用法简单：如 Cookies.get (“token”)

## 实现思路  
![status](https://github.com/Pidbid/python_chat/static/image/ddd.png)
后台采用 python 的 fastapi 作为框架（其实在整个实现的过程中什么作为网页框架并不重要），通信协议采用 websocket，由于主要实现的是聊天的功能，其他的并不重要，所以就简单的不使用数据库的情况下进行设计。ok，那我们开始吧～
### 数据预设

#### 数据简介

一个简单的聊天功能，需要的数据有：用户数据，传输数据两方面

#### 用户数据简介

用户存储在 data 文件夹下的 users.json 文件内

#### 传输数据简介

在采用 python 的 websockets_server 模块下，不需要关心 websocket 传输的流数据，只需要关注发送的字符串数据即可。

1) 用户登录数据

  {"status":"login","name":"wicos","avatar":"static/image/user.png"}
2) 用户登出数据

 {"status":"logout","name":"wicos"}
3) 用户聊天数据

 {"status":"chat","from":"wicos1","to":"wicos","data":"发送的其他信息"}
##  详细流程
![流程](https://github.com/Pidbid/python_chat/static/image/ddd.png)  
###  服务端流程  

#### ws 服务端主流程

服务端的主流程运行在一个子线程内，用户打开 ws 连接后，将用户的连接实例存储，存储之后等待用户的登录信息，之后更新再已存储的用户变量内，如果登出，则在用户变量内删除该用户实例。如果用户发送的 status 为 chat 的 json 数据，则将该信息放入另外一个子线程内，该子线程循环的将 “数据池” 内的聊天消息发送给在线且用户名符合的用户。

#### ws 服务端循环流程

循环流程运行在另外一个线程内，在该循环流程内，实时监控是否有用户发送消息至 “消息池”，如果有的话就将消息发送给符合的用户。

### ws 用户端流程

在用户登录后，使用 reconnect_websocket 的 js 库进行 ws 链接，发送登录信息，之后开始聊天流程

### 截图介绍
![login page](https://github.com/Pidbid/python_chat/static/image/ccc.png)  
![chat page 1](https://github.com/Pidbid/python_chat/static/image/aaa.png)  
![chat page 2](https://github.com/Pidbid/python_chat/static/image/bbb.png)  

## To do  
- 未来要做的事还没想好


## 鸣谢
- 登陆界面来自：https://gitee.com/QH_ayang/login.git