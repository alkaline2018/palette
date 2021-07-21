import multiprocessing
import os

from pymongo import UpdateOne

from env import db_conn_bak
from palette import Palette
from util import convert_image_insert

ab_path = os.path.dirname(os.path.abspath(__file__))
sp_mongo = db_conn_bak.SpspMongoDB()


def list_chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def make_conver_image_and_return_query_list(_image_dict_list):
    update_one_query_list = []
    for image_dict in _image_dict_list:
        image_path = image_dict['path']
        image_id = image_dict['_id']
        filter_query = {"_id": image_id}
        update_query = None
        try:
            # TODO 경로 변경 필요
            url = "http://192.168.0.20:9090" + image_path
            palette = Palette(url)
            n_path = os.path.join(ab_path, "../public/images", "." + image_path)
            n_dir = os.path.dirname(n_path)
            #
            if not os.path.exists(n_dir):
                os.makedirs(n_dir)

            # TODO: 2. 이미지경로를 통해 변형 이미지를 만들어 (4종류) O
            #   20번 서버 D:\spsp\images 에 저장한다. docker 로 작업하면 해결
            # TODO: 3. 변형이미지에 대한 내용을 image_convert collection 에 insert 한다. O
            # 현재는 test 이기 때문에 local에 저장한다.
            convert_image_insert(palette, n_path, image_path, image_id, sp_mongo)
            update_query = {"$set": {"convert_status": 1}}
        #
        except Exception as e:
            update_query = {"$set": {"convert_status": 2}}
            print(f"error: {e}")
        finally:
            # TODO: 4. image_collection 에 convert_status를 넣어 작업여부를 판단케 한다 O
            update_one_query = UpdateOne(filter_query, update_query)
            update_one_query_list.append(update_one_query)
    return update_one_query_list

if __name__ == "__main__":
    # TODO: 1. 기존 image_collection 에서 convert_status가 없는 이미지경로만을 불러온다. O
    PROCESS_NUMBER = 10
    MULTI_PROCESSING_POOL = multiprocessing.Pool(processes=PROCESS_NUMBER)

    image_collection = sp_mongo.image_collection
    image_query = {"convert_status": {"$exists": False}}
    image_projection = {"path": 1}
    while True:
        image_cursor = image_collection.find(image_query, image_projection).limit(1000)
        image_dict_list = list(image_cursor)
        if not image_dict_list:
            break
        chunk_list = list_chunk(image_dict_list, 100)
        query_list_list = MULTI_PROCESSING_POOL.map(make_conver_image_and_return_query_list, chunk_list)
        for query_list in query_list_list:
            image_collection.bulk_write(query_list)





