#!/usr/bin/python
import re

import psycopg2.extras
import logging
from pymongo import MongoClient
from env import config
from logs.nice_log import NiceLog
import psycopg2 as pg
import pandas as pd
import pymongo as pm


class DB_conn_2():

    def __init__(self):
        self.post_params = config.config()
        self.mongo_params = config.config(section='mongodb')
        self.mongo_nice_params = config.config(section='mongodb_nice')
        self.mongo_finace_params = config.config(section='mongodb_finance')
        self.mongo_client = self.mongo_client_connect(self.mongo_params)
        self.mongo_db = self.mongo_db_connect(self.mongo_params)

    def connect(self):
        connection = pg.connect(**self.post_params, cursor_factory=pg.extras.DictCursor)
        return connection

    def execute(self, sql, params={}):
        with self.connect() as connection:
            with connection.cursor(cursor_factory=pg.extras.DictCursor) as cursor:
                cursor.execute(sql, params)

    def mongo_client_connect(self, params):
        mongo_client = MongoClient(host=params['host'], port=int(params['port']),
                                   unicode_decode_error_handler='ignore')
        return mongo_client

    def mongo_db_connect(self, params):
        db = self.mongo_client[params['database']]
        return db

    def mongo_collection_connect(self):
        collection = self.mongo_db[self.mongo_params['collection']]
        return collection

    def mongo_nice_collection_connect(self):
        collection = self.mongo_db[self.mongo_nice_params['collection']]
        return collection

    def mongo_finance_collection_connect(self):
        collection = self.mongo_db[self.mongo_finace_params['collection']]
        return collection

    def select_fran_dict(self):
        cur = self.connect().cursor()
        sql = 'SELECT * FROM tb_sys_fran_dict WHERE active = TRUE ORDER BY brand_cd '
        cur.execute(sql)
        fran_dict_all = cur.fetchall()
        return fran_dict_all

    def si(self):
        cur = self.connect().cursor()
        sql = 'SELECT sigungu FROM si_gun_gu_ediya ORDER BY sigungu'
        cur.execute(sql)
        si = cur.fetchall()
        return si

    def select_tb_address(self):
        cur = self.connect().cursor()
        sql = "SELECT si_do || ' ' ||gun_gu || ' ' ||dong_lee  AS addr " \
              "FROM tb_addr_info " \
              "WHERE si_do_short_nm = '서울' " \
              "UNION ALL SELECT DISTINCT si_do || ' ' || gun_gu  AS addr FROM tb_addr_info " \
              "WHERE si_do_short_nm <> '서울';"
        cur.execute(sql)
        si = cur.fetchall()
        return si

    def select_finance(self):
        cur = self.connect().cursor()
        sql = "SELECT * " \
              "FROM tb_sys_finance_dict " \
              "WHERE sub_category NOT LIKE '%카드%' " \
              "AND active is TRUE " \
              "AND category_have = 0" \
              "ORDER BY sub_category,finance_nm"

        cur.self.execute(sql, )
        finance = cur.fetchall()
        return finance

    def select_finance_not(self):
        cur = self.connect().cursor()
        sql = "SELECT * " \
              "FROM tb_sys_finance_dict " \
              "WHERE sub_category NOT LIKE '%카드%' " \
              "AND active is TRUE " \
              "AND category_have = 1" \
              "ORDER BY sub_category,finance_nm"

        cur.self.execute(sql, )
        finance = cur.fetchall()
        return finance

    def select_finance_card(self):
        cur = self.connect().cursor()
        sql = "SELECT * FROM tb_sys_finance_dict WHERE sub_category LIKE '%카드%' AND active is TRUE ORDER BY sub_category,finance_nm"

        # sql = 'SELECT * FROM tb_sys_finance_dict WHERE SUB_CATEGORY LIKE "%카드%"'
        cur.self.execute(sql, )
        finance = cur.fetchall()
        return finance

    def select_fran_dict_by_id(self, brand_cd):
        cur = self.connect().cursor()
        sql = 'SELECT * FROM tb_sys_fran_dict WHERE brand_cd = %s and active = TRUE'
        cur.self.execute(sql, (brand_cd,))
        fran_dict_one = cur.fetchone()
        return fran_dict_one

    def select_fran_dict_by_view_way(self, view_way):
        cur = self.connect().cursor()
        sql = 'SELECT * FROM tb_sys_fran_dict WHERE view_way = %s and active = TRUE'
        cur.self.execute(sql, (view_way,))
        fran_dict = cur.fetchall()

        # fran_dict['total'] = len(fran_dict['fran_data'])
        return fran_dict

    # postgres의 주소 정제 데이터를 불러오는 함수
    def select_add_preprocess_data(self):
        con = self.connect()  # 유의어 사전이랑 연결
        sql = 'SELECT * FROM tb_add_preprocess_data'
        dic = pd.read_sql_query(sql, con)  # 몽고디비 명령어 입니다. 유의어 사전의 모든 내용을 가져오는 명령어 입니다.
        con.close()
        return dic

    # select_add_preprocess_data_by_gubun
    def select_add_preprocess_data_by_gubun(self, gubun):
        cur = self.connect().cursor()
        sql = 'SELECT * FROM tb_add_preprocess_data WHERE gunun like %s'
        cur.self.execute(sql, (gubun,))
        all_change = cur.fetchall()
        cur.close()
        return all_change

    def select_finance_group_by_finance_category(self, finance_nm, category, search_category):
        collection = self.mongo_finance_collection_connect()
        # query = {'addr': {'$nin': ['', None]}, 'finance_nm': finance_nm, 'category': {'$regex': '.*' + category + '.*'}}
        pipeline = []
        if search_category is True:
            pipeline = [
                {"$match":
                    {
                        'addr': {'$nin': ['', None]},
                        'finance_nm': finance_nm,
                        'category': {'$regex': '.*' + category + '.*'}
                    }
                },
                {"$group":
                    {
                        "_id":
                            {
                                "tel": "$tel",
                                "addr": "$addr",
                                "store_nm": "$store_nm",
                                "category": "$category",
                                "finance_nm": "$finance_nm"
                            }
                    }
                },
                {
                    "$project": {
                        "finance_nm": "$_id.finance_nm",
                        "store_nm": "$_id.store_nm",
                        "addr": "$_id.addr",
                        "tel": "$_id.tel",
                        "category": "$_id.category",
                        "_id": 0
                    }
                },
                {
                    "$sort": {
                        "finance_nm": 1,
                        "addr": 1
                    }
                }
            ]
        elif search_category is False:
            pipeline = [
                {"$match":
                    {
                        'addr': {'$nin': ['', None]},
                        'finance_nm': finance_nm,
                        'store_nm': {'$regex': '.*' + finance_nm + '.*'}
                    }
                },
                {"$group":
                    {
                        "_id":
                            {
                                "tel": "$tel",
                                "addr": "$addr",
                                "store_nm": "$store_nm",
                                "category": "$category",
                                "finance_nm": "$finance_nm"
                            }
                    }
                },
                {
                    "$project": {
                        "finance_nm": "$_id.finance_nm",
                        "store_nm": "$_id.store_nm",
                        "addr": "$_id.addr",
                        "tel": "$_id.tel",
                        "category": "$_id.category",
                        "_id": 0
                    }
                },
                {
                    "$sort": {
                        "finance_nm": 1,
                        "addr": 1
                    }
                }
            ]
        # results = collection.find(query, {'_id': 1, 'yyyymm': 1, 'finance_nm': 1,'category': 1, 'store_nm': 1, 'tel': 1, 'addr': 1})
        results = collection.aggregate(pipeline)

        return results

    def select_finance_group_by_finance_nm(self, finance_nm):
        collection = self.mongo_finance_collection_connect()
        # query = {'addr': {'$nin': ['', None]}, 'finance_nm': finance_nm, 'category': {'$regex': '.*' + category + '.*'}}
        pipeline = [
            {"$match":
                {
                    'addr': {'$nin': ['', None]},
                    'finance_nm': {'$regex': '.*' + finance_nm + '.*'}
                }
            },
            {"$group":
                {
                    "_id":
                        {
                            "tel": "$tel",
                            "addr": "$addr",
                            "store_nm": "$store_nm",
                            "category": "$category",
                            "finance_nm": "$finance_nm"
                        }
                }
            },
            {
                "$project": {
                    "finance_nm": "$_id.finance_nm",
                    "store_nm": "$_id.store_nm",
                    "addr": "$_id.addr",
                    "tel": "$_id.tel",
                    "category": "$_id.category",
                    "_id": 0
                }
            },
            {
                "$sort": {
                    "finance_nm": 1,
                    "addr": 1
                }
            }
        ]

        # results = collection.find(query, {'_id': 1, 'yyyymm': 1, 'finance_nm': 1,'category': 1, 'store_nm': 1, 'tel': 1, 'addr': 1})
        results = collection.aggregate(pipeline)

        return results

    # 몽고 디비의 데이터를 가져오는 함수
    def mongo_db_data(self, brand_cd):
        collection = self.mongo_collection_connect()
        query = {'f_addr': {'$nin': ['', None]}, 'brand_cd': brand_cd}
        results = collection.find(query, {'_id': 1, 'brand_cd': 1, 'yyyymm': 1,
                                          'source': 1, 'brand_nm': 1, 'store_nm': 1,
                                          'addr': 1, 'tel': 1})
        data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return data

    def update_nice_franchise_e2on_key(self, data):
        collection = self.mongo_nice_collection_connect()
        query = {"brand_cd": data["brand_cd"], "store_nm": data['f_name'], "addr": data['f_addr'], "tel": data['f_tel']}
        new_data = {"$set": {"e2on_key": data['e2on_key']}}
        collection.update_one(query, new_data)

    def update_nice_franchise_rm_addr_store_nm(self, data):
        collection = self.mongo_nice_collection_connect()
        query = {"store_key": data["store_key"]}
        new_data = {"$set": {"rm_store_nm": data['rm_store_nm'], "rm_addr": data['rm_addr']}}
        collection.update_one(query, new_data)

    # 몽고 디비의 데이터를 가져오는 함수
    def mongo_group_by_clct(self):
        collection = self.mongo_collection_connect()
        query = [
            {
                "$match": {
                    "$and": [
                        {
                            "brand_cd": {
                                "$lt": 500
                            }
                        },
                        {
                            "brand_cd": {
                                "$gt": 0
                            }
                        },
                        {
                            "f_name": {
                                "$exists": True
                            },
                            "f_addr": {
                                "$exists": True
                            }
                        }
                    ]
                }
            },
            {
                "$group": {
                    "_id": {
                        "e2on_key": "$e2on_key",
                        "f_tel": "$f_tel",
                        "brand_cd": "$brand_cd",
                        "f_name": "$f_name",
                        "f_addr": "$f_addr"
                    }
                }
            },
            {
                "$project": {
                    "brand_cd": "$_id.brand_cd",
                    "f_name": "$_id.f_name",
                    "f_addr": "$_id.f_addr",
                    "f_tel": "$_id.f_tel",
                    "e2on_key": "$_id.e2on_key",
                    "_id": 0
                }
            }
        ]
        results = collection.aggregate(query)
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return results

    # 몽고 디비의 데이터를 가져오는 함수
    def mongo_nice_all_data(self):
        collection = self.mongo_nice_collection_connect()
        query = {
            "$and": [
                {
                    "store_key": {
                        "$exists": True
                    }
                },
                {
                    "e2on_key": {
                        "$exists": False
                    }
                },
                {
                    "brand_cd": {
                        "$lt": 500
                    }
                }
            ]
        }
        results = collection.find(query, )
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return results

    # all_change
    def mongo_db_data_all_change(self, change):
        collection = self.mongo_collection_connect()
        query = {"f_addr": change[0]}
        if change[1] is None:
            change[1] = ""
        new_data = {"$set": {"f_addr": change[1]}}
        collection.update_many(query, new_data)
        return None

    # gubun
    def mongo_db_update_gubun(self, change):
        collection = self.mongo_collection_connect()
        query = {"first_addr": change[0]}
        if change[1] is None:
            change[1] = ""
        new_data = {"$set": {"gubun": change[1]}}
        collection.update_many(query, new_data)
        return None

    def mongo_db_update(self, data):
        collection = self.mongo_collection_connect()
        for d, k in data.iterrows(self):
            query = {"_id": k._id}
            new_data = {"$set": {"f_name": k.f_name,
                                 "f_addr": k.f_addr,
                                 "f_tel": k.f_tel}}
            collection.update_many(query, new_data)
        return None

    # 몽고 디비의 데이터를 가져오는 함수
    def select_mongo_db_nin_number(self):
        collection = self.mongo_collection_connect()
        q = {
            "$and": [
                {
                    "f_addr": {
                        "$nin": [
                            re.compile('[0-9]')
                        ]
                    }
                },
                {
                    "f_addr": {
                        "$exists": True
                    }
                },
                {
                    "brand_cd": {
                        "$lt": 500
                    }
                }
            ]
        }
        results = collection.find(q)
        for result in results:
            print(result['f_addr'])
        return results

    def close_client(self):
        self.mongo_client.close()

    # 실제 사용 함수 끝==========================================================================================

    def insert_fran_info(self, item):
        """ insert table  """
        sum = 0
        fields = ', '.join(item.keys())
        values = ', '.join(['%%(%s)s' % x for x in item])
        sql = 'INSERT INTO tb_xpath_nice_data_201912 (%s) VALUES (%s)' % (fields, values)
        self.execute(sql, item)
        sum += 1
        return sum

    # def insert_fran_info_test2(brand_cd=None, brand_nm=None, source=None,
    #                            store_nm=None, tel=None, yyyymm=None,
    #                            addr=None, gubun=None):
    #     """ insert table  """
    #     sum = 0
    #     sql = 'INSERT INTO tb_xpath_nice_data ' \
    #                 'brand_cd, brand_nm, source,store_nm, tel, yyyymm, addr, gubun ' \
    #           'VALUES ' \
    #                 '(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #     param = (brand_cd, brand_nm, source, store_nm, tel, yyyymm, addr, gubun)
    #     self.execute(sql, param)
    #     sum += 1
    #     return sum
