#!/usr/bin/python
import re

from pymongo import MongoClient, InsertOne
from env import config
import psycopg2 as pg
import psycopg2.extras

from imageEnums import Duplicate_check

class Postgresql:
    def __init__(self):
        self.params = config.config()

    def connect(self):
        self.connection = pg.connect(**self.params, cursor_factory=psycopg2.extras.DictCursor)
        # self.connection = pg.connect(**self.params)

    def get_connect(self):
        return self.connection

    def close(self):
        self.connection.commit()
        self.connection.close()

    def execute(self, sql, params={}):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as self.cursor:
            self.cursor.execute(sql, params)

    def find_image(self, item):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        values = 'and '.join([x + '=%%(%s)s' % x for x in item])
        sql = "SELECT * " \
              "FROM image " \
              "WHERE %s;" % (values)
        cur.execute(sql, (item))
        result = cur.fetchone()
        cur.close()
        return result

    def find_all_image(self):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * " \
              "FROM image;"
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        return results

    def insert_image(self, item):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        """ insert table  """
        sum = 0
        fields = ', '.join(item.keys())
        values = ', '.join(['%%(%s)s' % x for x in item])
        sql = 'INSERT INTO image (%s) VALUES (%s)' % (fields, values)
        print(sql)
        cur.execute(sql, (item))
        cur.close()
        sum += 1
        return sum

class SpspMongoDB:

    def __init__(self):
        params = config.config(section='mongodb')
        self.mongoClient = self.mongo_client_connect()
        self.db = self.mongoClient[params['database']]
        self.clct_collection = self.db[params['clct_collection']]
        self.image_collection = self.db[params['image_collection']]
        self.image_collection2 = self.db[params['image_convert_collection']]

    def mongo_client_connect(self):
        params = config.config(section='mongodb')
        mongoClient = MongoClient(host=params['host'], port=int(params['port']), unicode_decode_error_handler='ignore')
        return mongoClient

    def close(self):
        self.mongoClient.close()

    # TODO: collection 은 parameter로 변경되어 작동할 것
    def find_clct_images_by_check_type(self,
                                       _collection,
                                       _check_types=[Duplicate_check.ALL_DOWNLOAD_IMAGE.value],
                                       # _check_types=[Duplicate_check.DUPLICATED.value, Duplicate_check.ORIGINAL.value],
                                       _limit=10):
        query = {
            "imagesStatus": {
                "$in": _check_types
            }
        }
        projection = {
            "_id": 1,
            "images": 1,
            "channel": 1
        }

        results = _collection.find(query, projection).limit(_limit)
        return list(results)

    def find_image(self, _query):
        result = self.image_collection.find_one(_query, )
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return result

    def find_image_by_hash(self, hash):
        query = {'hash': hash}
        result = self.image_collection.find_one(query, )
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return result

    def update_clct_by_imageid(self, _query, _image_dict):
        result = self.clct_collection.update_one(_query, {"$set": _image_dict})
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return result

    def insert_image(self, _image_dict):
        _id = self.image_collection.insert_one(_image_dict)
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return _id

    def insert_image2(self, _image_dict):
        _id = self.image_collection2.insert_one(_image_dict)
        # data = pd.DataFrame([result for result in results]).reset_index(drop=1)
        return _id

    def get_insert_image_query(self, _image_dict):
        return InsertOne(_image_dict)

    def bulk_write_at_image(self, _querys):
        return self.image_collection.bulk_write(_querys)

    def bulk_write_at_clct(self, _querys):
        self.clct_collection.bulk_write(_querys)





