#!/usr/bin/python
import re

from pymongo import MongoClient, InsertOne
from env import config

from remove_duplicated import Duplicate_check

class SpspMongoDB:

    def __init__(self):
        params = config.config(section='mongodb')
        self.mongoClient = self.mongo_client_connect()
        self.db = self.mongoClient[params['database']]
        self.clct_collection = self.db[params['clct_collection']]
        self.image_collection = self.db[params['image_collection']]

    def mongo_client_connect(self):
        params = config.config(section='mongodb')
        mongoClient = MongoClient(host=params['host'], port=int(params['port']), unicode_decode_error_handler='ignore')
        return mongoClient

    def close(self):
        self.mongoClient.close()

    def find_clct_images_by_check_type(self,
                                       _check_types=[Duplicate_check.DUPLICATED.value, Duplicate_check.ORIGINAL.value, Duplicate_check.ERROR.value],
                                       # _check_types=[Duplicate_check.DUPLICATED.value, Duplicate_check.ORIGINAL.value],
                                       _limit=10):
        query = {
            "duplicateCheck": {
                "$nin": _check_types
            }
        }
        # TODO: 추후엔 thumbnailUrl 이미지에서 downloadPaths 로 변경될 예정
        projection = {
            "_id": 1,
            "thumbnailUrl": 1
        }

        results = self.clct_collection.find(query, projection).limit(_limit)
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

    def get_insert_image_query(self, _image_dict):
        return InsertOne(_image_dict)

    def bulk_write_at_image(self, _querys):
        return self.image_collection.bulk_write(_querys)

    def bulk_write_at_clct(self, _querys):
        self.clct_collection.bulk_write(_querys)





