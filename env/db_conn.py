#!/usr/bin/python
from env.common_db_conn import MongoDB

class ImageMongoDB(MongoDB):

    def print_db_name(self):
        print(self.get_db().name)





