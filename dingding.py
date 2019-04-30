#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/25 0025'

"""

import json
from datetime import datetime

import requests


class DingMsg():
    def __init__(self):
        self.HEADERS = {
            "Content-Type": "application/json ;charset=utf-8 "
        }

    def parse_data(self, data):
        self.keyword = data.get('keyword')
        self.img_src = data.get('img_src')
        self.title = data.get('title')
        self.xianyu_url = data.get('pic_href')
        self.pub_time = data.get('pub_time')
        self.price = data.get('price')
        self.location = data.get('location')
        self.desc = data.get('desc')

    def text_msg_content(self):
        self.parse_data(self.data)
        text = '{title}\n{xianyu_url}\n关键字：{keyword}\n价格：{price}  \n时间:{pub_time}'.format(title=self.title,
                                                                                          xianyu_url=self.xianyu_url,
                                                                                          keyword=self.keyword,
                                                                                          price=self.price,
                                                                                          pub_time=self.pub_time)

        return {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                # "atMobiles": [
                # ],
                "isAtAll": True
            }
        }

    def link_msg_content(self):
        self.parse_data(self.data)
        # 链接的话，手机端没法直接点进去展示，电脑端可以展示
        link_text = '{title}\n时间：{pub_time}'.format(title=self.title, pub_time=self.pub_time)
        return {
            "msgtype": "link",
            "link": {
                "text": link_text,
                "title": '闲鱼"{}"最新商品消息'.format(self.keyword),
                "picUrl": self.img_src,
                "messageUrl": self.xianyu_url
            }
        }

    def markd_msg_content(self):
        markdown_content = ""
        for item in self.data:
            self.parse_data(item)
            markdown_content += "---------------------------------\n \n" \
                                "#### **关键字:** {keyword}\n" \
                                "###### 价格:{price} 时间:{pub_time}\n" \
                                "#### 标题:{title}\n" \
                                "#### 链接:[{xianyu_url}]({xianyu_url})\n".format(keyword=self.keyword, price=self.price,
                                                                                pub_time=self.pub_time,
                                                                                title=self.title,
                                                                                xianyu_url=self.xianyu_url)
        return {
            "msgtype": "markdown",
            "markdown": {
                "title": "新增闲鱼商品",
                "text": "## **新增闲鱼商品** \n" +
                        " ###### {} 发布\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + markdown_content
            },
            "at": {
                # "atMobiles": [
                #     "156xxxx8827",
                #     "189xxxx8325"
                # ],
                "isAtAll": True
            }
        }

    def check_msg_content(self):
        return {
            "msgtype": "text",
            "text": {
                "content": self.data
            },
            "at": {
                # "atMobiles": [
                # ],
                "isAtAll": True
            }
        }

    def send_msg(self, webhook_url, data, type):
        # 这里的message是你想要推送的文字消息三种格式 ：text_msg_content  link_msg_content  markd_msg_content
        self.data = data
        if type == 1:
            mesBody = self.text_msg_content()
        elif type == 2:
            mesBody = self.link_msg_content()
        elif type == 3:
            mesBody = self.markd_msg_content()
        else:
            mesBody = self.check_msg_content()
        MessageBody = json.dumps(mesBody)
        result = requests.post(url=webhook_url, data=MessageBody, headers=self.HEADERS)
        print(result.text)
        try:
            if result.json().get('errmsg') == 'ok':
                return True
            elif result.json().get('errmsg') == '消息中包含不合适的内容':
                return True
            else:
                return False
        except Exception as e:
            return False
