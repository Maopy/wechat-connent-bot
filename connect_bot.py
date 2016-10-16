#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import itchat
from itchat.content import TEXT
import thread
import time
import datetime
import re

#########
#log
import logging
LOG_FILE = "/tmp/wechat_log.log"
logging.basicConfig(filename=LOG_FILE,level=logging.INFO)
logger = logging.getLogger(__name__)
handler=logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
#########

# todo ： group1 和group2硬编码部分抽象为函数
# todo：targetGroupIds = []
group1_id = None
group2_id = None
group1 = 'ReactJS中文'
group2 = 'ReactJS 2群'
group1_msg_list=[]
group2_msg_list=[]

def change_function():
  global group1_msg_list
  global group2_msg_list
  global group1_id
  global group2_id

  if  group1_msg_list and group1_id:  # 一群消息队列不为空且已经获取到一群ID
    print(group1_msg_list)
    for msg in group1_msg_list:
      message = '@{}：\n{}'.format(msg['ActualNickName'],msg['Text'])
      itchat.send_msg(message,group2_id) # 完成主动推送
    group1_msg_list = []
  if  group2_msg_list and group2_id:  # 二群消息队列不为空且已经获取到二群ID
    print(group2_msg_list)
    for msg in group2_msg_list:
      message = '@{}：\n{}'.format(msg['ActualNickName'],msg['Text'])
      itchat.send_msg(message,group1_id) # 完成主动推送
    group2_msg_list = []
  @itchat.msg_register(TEXT, isGroupChat=True)  # 筛选群聊
  def simple_reply(msg):
    global group1_msg_list
    global group2_msg_list
    global group1_id
    global group2_id

    # 需要判断是否处理消息，只处理目标群消息
    if msg['FromUserName'] == group1_id: # 针对性处理消息
      print('微信群{}连接完毕'.format(group1))
      # 来自群1消息，加入消息队列
      if '/bot/h' in msg["Text"]:
        response='Hi @{}：\nmessage bot是个信使机器人，将使1、2群消息互通'.format(msg['ActualNickName'])
        print(response,group1_id)
      else:
        group1_msg_list.append(msg)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info((now,group1,msg['ActualNickName'],msg["Text"]))

    if not group1_id:
      # 如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
      group1_instance = itchat.search_chatrooms(name=group1)
      if group1_instance:
        group1_id = group1_instance[0]['UserName']
        print('发现{}id，信使机器人已激活: )'.format(group1),group1_id)

    if msg['FromUserName'] ==  group2_id:
      print('微信群{}连接完毕'.format(group2))
      now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if '/bot/h' in msg["Text"]:
        response='Hi @{}：\nmessage bot是个信使机器人，将使1、2群消息互通'.format(msg['ActualNickName'])
        print(response,group2_id)
      else:
        group2_msg_list.append(msg)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info((now,group2,msg['ActualNickName'],msg["Text"]))
    if not group2_id:
      group2_instance = itchat.search_chatrooms(name=group2)
      if group2_instance:
        group2_id = group2_instance[0]['UserName']
        print('发现{}id，信使机器人已激活: )'.format(group2),group2_id)

itchat.auto_login(enableCmdQR=2,hotReload=True)
thread.start_new_thread(itchat.run, ())

while 1:
  change_function()
  time.sleep(1)
