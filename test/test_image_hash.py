import unittest

import requests
from PIL import Image
import imagehash
import random
import uuid
import psycopg2 as pg

def diff_percent(hash1, hash2, type):
    hash_len = 8
    if type == 2:
        hash_len = 14

    _hash1 = imagehash.hex_to_flathash(hash1, hash_len)
    _hash2 = imagehash.hex_to_flathash(hash2, hash_len)
    return _hash1.__sub__(_hash2) / hash_len ** 2

def diff_percent_by_image(image_ori, image_compare_list):
    hash_size = 10
    result_list = []
    i = 0
    for image_compare in image_compare_list:
        i = i + 1
        # _a_hash1 = imagehash.average_hash(image_ori, hash_size)
        # _a_hash2 = imagehash.average_hash(image_compare, hash_size)
        _p_hash1 = imagehash.phash(image_ori, hash_size)
        _p_hash2 = imagehash.phash(image_compare, hash_size)
        # _w_hash1 = imagehash.whash(image_ori, hash_size)
        # _w_hash2 = imagehash.whash(image_compare, hash_size)
        # _d_hash1 = imagehash.dhash(image_ori, hash_size)
        # _d_hash2 = imagehash.dhash(image_compare, hash_size)
        # _c_hash1 = imagehash.colorhash(image_ori, hash_size)
        # _c_hash2 = imagehash.colorhash(image_compare, hash_size)
        # print(len(_c_hash1.hash))
        # print(len(_p_hash1.hash))
        p = (_p_hash1.__sub__(_p_hash2)) / hash_size ** 2 * 100
        # a = (_a_hash1.__sub__(_a_hash2)) / hash_size ** 2 * 100
        # w = (_w_hash1.__sub__(_w_hash2)) / hash_size ** 2 * 100
        # d = (_d_hash1.__sub__(_d_hash2)) / hash_size ** 2 * 100
        # c = (_c_hash1.__sub__(_c_hash2)) / 14 ** 2 * 100
        result = {
            "index": i,
            "p_diff_percent":p,
            # "a_diff_percent":a,
            # "w_diff_percent":w,
            # "d_diff_percent":d,
            # "c_diff_percent":c
        }
        result_list.append(result)
    return result_list

class MyTestCase(unittest.TestCase):
    def test_diff_percent(self):
        image_0 = Image.open('../static/image/cafe.jpg')
        image_1 = Image.open('../static/image/cafe_1.jpg')
        image_2 = Image.open('../static/image/cafe_2.jpg')
        image_3 = Image.open('../static/image/cafe_3.jpg')
        image_4 = Image.open('../static/image/cafe_4.jpg')
        image_5 = Image.open('../static/image/cafe_5.jpg')
        image_6 = Image.open('../static/image/cafe_6.jpg')
        image_11 = Image.open('../static/image/cafe_11.jpg')
        image_list = [
            image_1,
            image_2,
            image_3,
            image_4,
            image_5,
            image_6,
            image_11,
            image_0
        ]
        results = diff_percent_by_image(image_0, image_list)
        print(results)

    def test_hex_format(self):

        hexstr = 'fc0d000000ff0000000000020000'
        hashsize = 8
        print(int(hexstr, 16))
        hash_size = int(len(hexstr) * 4 / (hashsize))
        print(hash_size)
        a = '{:0>{width}b}'.format(int(hexstr, 16), width=hash_size * hashsize)
        print(a)
        print(a.__len__())
    def test_hasharray_hashlist(self):
        image_1 = Image.open('../static/image/cafe.jpg')
        __hash = imagehash.whash(image_1, 8)
        image_2 = Image.open('../static/image/cafe_3.jpg')
        _hash = imagehash.whash(image_2, 8)
        hash_str = _hash.__str__()
        print(f'_hash: {hash_str}')
        _hash2 = imagehash.hex_to_flathash(hash_str, 8)
        hash_str2 = _hash2.__str__()
        print(f'_hash2: {hash_str2}')
        print(len(__hash.hash))
        print(_hash2.__sub__(__hash)/14**2)

        imagehash.phash()
        imagehash.dhash()
        imagehash.average_hash()
        imagehash.colorhash()

    def test_make_hash(self):
        conn = pg.connect(database="nicedata_franchise", user='cloud3', password='cloud3', host='localhost', port='5444')
        cursor = conn.cursor()
        hash_list = []
        for i in range(100000):
            hash = "%25x" % random.getrandbits(100)
            hash_list.append((hash,))

        cursor.executemany('INSERT INTO public.test_hash (hash) VALUES (%s)', hash_list)
        conn.commit()
        cursor.close()
        conn.close()

    def test_something(self):
        image_1 = Image.open('../static/image/ho.jpg')
        # image_1 = Image.open(requests.get('https://www.blockmedia.co.kr/wp-content/uploads/2021/02/%EC%9D%BC%EB%A1%A0%EB%A8%B8%EC%8A%A4%ED%81%AC_%EC%A0%95%EC%82%AC%EA%B2%A9%ED%98%95.jpg', stream=True).raw)
        # image_1 = Image.open(requests.get('https://ichi.pro/assets/images/max/724/0*tndyQCT-GkJxEN_j.jpg', stream=True).raw)

        image_2 = Image.open('../static/image/ho2.jpg')
        # image_2 = Image.open(requests.get('https://storage.googleapis.com/talkingheads-rosebudai/default_persons/default_tokkingheads/Elon.png', stream=True).raw)
        hash = imagehash.dhash(image_1)
        hash2 = imagehash.dhash(image_2)

        # hash1 = imagehash.dhash(Image.open('../static/image/cafe_11.jpg'), 10)
        # a_hash = imagehash.colorhash(image_1, 10)
        # a_hash2 = imagehash.colorhash(image_2, 10)
        a_hash = imagehash.colorhash(image_1)
        a_hash2 = imagehash.colorhash(image_2)

        # hash3 = imagehash.dhash(Image.open('../static/image/cafe_6.jpg'), 10)
        print(len(hash.hash)**2)
        print(f"d_hash: {hash}")
        print(f"d_hash: {hash2}")
        list1 = hash.hash.flatten()
        list2 = hash2.hash.flatten()
        print(f"dict(hash): {dict(hash)}")
        print(f"{list1 - list2}")
        print((hash - hash2))

        print((hash - hash2)/len(hash.hash)**2)

        print(len(a_hash.hash)**2)
        print(f"colorhash: {a_hash}")
        print(f"colorhash: {a_hash2}")
        print((a_hash - a_hash2)/len(a_hash.hash)**2)
        # self.assertEqual(hash, hash2)


if __name__ == '__main__':
    unittest.main()
