#!/usr/bin/python
from pymongo import MongoClient, UpdateOne, UpdateMany, DeleteMany, DeleteOne
from env import config
import psycopg2.extras

import psycopg2 as pg

# 상속해서 class 새롭게 만들 것
class MongoDB(object):

    # NOTE: 공통
    def __init__(self, _section_name):
        self.CONFIG = config.config(section=_section_name)
        self.CLIENT = MongoClient(host=self.CONFIG['host'], port=int(self.CONFIG['port']),
                                  unicode_decode_error_handler='ignore')
        self.DB = self.CLIENT[self.CONFIG['database']]
        self.COLLECTION = self.DB[self.CONFIG['collection']]

    def close(self):
        try:
            self.CLIENT.close()
        except AttributeError:  # isn't closable
            print('Not closable.')
            return True  # exception handled successfully

    def get_config(self):
        return self.CONFIG

    def get_db(self):
        return self.DB

    def get_collection(self):
        return self.COLLECTION

    def make_collection(self, _name):
        return self.DB[_name]

    def _get_db(self, _db=None):
        if _db is None:
            _db = self.DB
        return _db

    def _get_collection(self, _collection=None):
        if _collection is None:
            _collection = self.COLLECTION
        return _collection

    def set_db(self, _name):
        self.DB = self.CLIENT[_name]

    def set_collection(self, _name):
        self.COLLECTION = self.DB[_name]

    def get_collection_names(self, _db=None):
        return self._get_db(_db=_db).list_collection_names()

    def get_sorted_collection_names(self, _db=None):
        return sorted(self.get_collection_names(_db=_db))

    def bulk_write(self, _query_list, _collection=None):
        self._get_collection(_collection).bulk_write(_query_list)

    def find(self, _query={}, _projection=None, _collection=None, _limit=None, _sort_dict=None):
        cursor = self._get_collection(_collection=_collection).find(_query, _projection)
        cursor = self._plus_limit(_cursor=cursor, _limit=_limit)
        cursor = self._plus_sort(_cursor=cursor, _sort_dict=_sort_dict)
        return cursor

    def _plus_limit(self, _cursor, _limit=None):
        if _limit is not None:
            return _cursor.limit(_limit)
        else:
            return _cursor

    def _plus_sort(self, _cursor, _sort_dict=None):
        if _sort_dict is not None:
            key_or_list = _sort_dict['key_or_list']
            direction = None
            if 'direction' in _sort_dict:
                direction = _sort_dict['direction']
            return _cursor.sort(key_or_list=key_or_list, direction=direction)
        else:
            return _cursor

    def get_delete_one_query_by_id(self, _id):
        query = {"_id": _id}
        return DeleteOne(query)

    def get_update_one_query_by_id(self, _id, _data_dict):
        query = {"_id": _id}
        new_data = {"$set": _data_dict}
        return UpdateOne(query, new_data)


# NOTE: postgres
def connect():
    params = config.config()
    connection = pg.connect(**params, cursor_factory=pg.extras.DictCursor)
    return connection

def execute(sql, params={}):
    with connect() as connection:
        with connection.cursor(cursor_factory=pg.extras.DictCursor) as cursor:
            cursor.execute(sql, params)