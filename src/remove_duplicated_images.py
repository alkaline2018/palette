import unittest

import requests
from PIL import Image
import imagehash
import random

from env import db_conn
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    # mypath = join('..', 'static', 'image', 'test')
    mypath = join('..', 'static', 'images')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles.__len__())
    for onlyfile in onlyfiles:
        path = join(mypath, onlyfile)
        # print(path)
        flag = None
        # path = '../static/image/cafe_3.jpg'
        url = 'https://storage.googleapis.com/talkingheads-rosebudai/default_persons/default_tokkingheads/Elon.png'
        if flag == 1:
            image = Image.open(requests.get(url, stream=True).raw)
        else:
            image = Image.open(path)
        _hash = imagehash.dhash(image, 10)
        _color_hash = imagehash.colorhash(image, 3)
        _a_hash = imagehash.average_hash(image)
        _d_hash_5 = imagehash.dhash(image, 5)
        _d_hash_7 = imagehash.dhash(image, 7)
        _d_hash_10 = imagehash.dhash(image, 10)
        print("_color_hash: ", len(_color_hash.hash))

        # db_conn.insert_image({"hash":_hash.tolist()})

        # result = db_conn.find_image_by_hash(_hash.__str__())
        # # print(_hash.__str__())
        # image_dict = {"hash": _hash.__str__(),
        #  "hash2": _d_hash_10.__str__(),
        #  "hash3": _d_hash_7.__str__(),
        #  "hash4": _d_hash_5.__str__(),
        #  "_color_hash": _color_hash.__str__(),
        #  "_a_hash": _a_hash.__str__(),
        #  "path": path}
        # if (result):
        #     print("동일")
        #     if (image_dict['hash'] != result['hash'] and image_dict['_color_hash'] == result['_color_hash']):
        #         print(f"image_dict: {image_dict}")
        #         print(f"===result: {result}")
        # else:
        #     db_conn.insert_image(image_dict)
        #     # print("없다 DB INSRET")
