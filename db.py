#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/25 0025'

"""
from pymongo import MongoClient, ASCENDING

# mongod.exe --logpath D:\mongodb\xianyudb\mongodb.log --logappend --dbpath D:\mongodb\xianyudb --directoryperdb --serviceName mongodbxy --install
ip = '127.0.0.1'
port = 27017


class MongoTime():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.xianyu
        self.collection = self.db.time
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def select_one(self, dict):
        return self.collection.find_one(dict)

    def delete(self, query_dict):
        self.collection.delete_one(query_dict)

    def delete_all(self, dict):
        self.collection.delete_many(dict)

    def update_time(self, key):
        self.collection.update({'flag': 1}, {'$set': {"time": key}})

    def update_type(self, key):
        self.collection.update({'flag': 1}, {'$set': {"type": key}})

    def count(self):
        self.collection.count_documents({})


class MongoKeyword():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.xianyu
        self.collection = self.db.keyword1
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def select_all(self, dict):
        return self.collection.find(dict)

    def select_one(self, dict):
        return self.collection.find_one(dict)

    def delete(self, query_dict):
        self.collection.delete_one(query_dict)

    def delete_all(self, dict):
        self.collection.delete_many(dict)

    def update_start(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 1}})

    def update_stop(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 0}})

    def update(self, dic):
        self.collection.update(dic)

    def count(self):
        self.collection.count_documents({})


class MongoProduct():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.xianyu
        self.collection = self.db.product
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def select(self, dict):
        return self.collection.find_one(dict)

    def delete(self, query_dict):
        self.collection.delete_one(query_dict)

    def delete_all(self, dict):
        self.collection.delete_many(dict)

    def update_start(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 1}})

    def update_stop(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 0}})

    def count(self):
        self.collection.count_documents({})


class MongoConfig():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.xianyu
        self.collection = self.db.config
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def select_one(self, dic):
        return self.collection.find_one(dic)

    def select_all(self):
        return self.collection.find()

    def delete(self, query_dict):
        self.collection.delete_one(query_dict)

    def delete_all(self, dict):
        self.collection.delete_many(dict)

    def update_start(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 1}})

    def update_stop(self, key):
        self.collection.update({'keyword': key}, {'$set': {"start": 0}})

    def count(self):
        return self.collection.count_documents({})

