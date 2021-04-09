#!/usr/bin/env python
import datetime
import time
import uuid
from enum import Enum


# from env.db_conn import SpspMongoDB
from palette import Palette, urlOrPath
from env import db_conn
import sys
import os
import shutil


class Duplicate_check(Enum):
    """
    HINT:
    :type ORIGINAL: 오리지날 이미지
    :type DUPLICATED: 오리지날 이미지에서 파생된 중복이미지
    :type ERROR: 원인을 알 수 없는 나머지 ERROR
    :type HASH_ERROR: 이미지 해시 생성중 발생한 ERROR
    :type IMAGE_INSERT_ERROR: 이미지 INSERT 중 발생한 ERROR
    :type IMAGE_SAVE_ERROR: 이미지 저장중 발생한 ERROR
    """
    ORIGINAL = 1
    DUPLICATED = 2
    ERROR = 3
    HASH_ERROR = 4
    IMAGE_INSERT_ERROR = 5
    IMAGE_SAVE_ERROR = 6


if __name__ == "__main__":
    stime = time.time()  # 시작시간
    results = []
    sp_mongo = db_conn.SpspMongoDB()

    try:
        # NOTE: 1. 몽고디비에서 thumbnailUrl or downloadPaths 중 이미지를 부른다.
        uncheck_images = sp_mongo.find_clct_images_by_check_type(_limit=5)
        # results = []
        # NOTE: 2. 이미지에서 imageHash 값을 추출한다.
        for uncheck_image in uncheck_images:
            try:
                # HINT: 하나의 문서에는 여러 장의 이미지가 있을 수 있다. 이에 여러 장의 이미지를 중복 처리한다.
                # TODO: 현재는 임의로 thumbnailUrl 로 잡았지만 추후 downloadPaths 로 변경한다.
                down_image_paths = [uncheck_image['thumbnailUrl'], uncheck_image['thumbnailUrl']]
                ids = []
                update_dict = {}

                ab_path = os.path.dirname(os.path.abspath(__file__))
                for down_image_path in down_image_paths:
                    # new 이미지
                    palette = Palette(down_image_path)
                    # get hash
                    image_dict = palette.get_defalut_hash_dict()
                    result = sp_mongo.find_image(image_dict)
                    if result:
                        # 해당 결과는 수집 collection 에 반영
                        ids.append(result['_id'])
                    else:
                        new_image_path = ''
                        if urlOrPath(down_image_path):
                            # HINT: url 을 바탕으로 이미지 이름 생성 jpg 저장 이유는 손실저장 방식이라 용량이 절감된다.
                            #   만약 원본 이미지에 가깝게 저장하고 싶다면 png로 저장 다만 저장 방식 때문에 용량이 크게 늘어날 수 있다.
                            # print("url")

                            new_image_path = "public/image/" + uuid.uuid3(uuid.NAMESPACE_URL, down_image_path).__str__() + ".jpg"
                            n_path = os.path.join(ab_path, "../" + new_image_path)

                            # 이미지 저장
                            palette.get_image().save(n_path)
                        else:
                            # TODO: 이미지 경로가 바뀌었으면 새롭게 저장하는 법도 바뀌어야 한다.
                            # print("path")
                            # temp 이미지 경로를 image로 변경
                            new_image_path = down_image_path.replace("temp", "image")
                            o_path = os.path.join(ab_path, "../" + down_image_path)
                            n_path = os.path.join(ab_path, "../" + new_image_path)
                            shutil.move(o_path, n_path)
                        # NOTE: 아래 내용에서 down_image_path 대신 변경된 new_image_path 로 넣어준다.
                        image_dict['path'] = new_image_path
                        # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
                        _id = sp_mongo.insert_image(_image_dict=image_dict)
                        ids.append(_id.inserted_id)

                update_dict['imageIds'] = ids
                update_dict['duplicateCheck'] = Duplicate_check.DUPLICATED.value
                result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)

            except Exception as e:
                result = sp_mongo.update_clct_by_imageid(
                    _query={"_id": uncheck_image['_id']},
                    _image_dict={'duplicateCheck': Duplicate_check.ERROR.value}
                )
                print(f"error1: {e}", flush=True)
    except Exception as e:
        print(f"error2: {e}", flush=True)
    finally:
        sp_mongo.close()
    # mongo client close
    etime = time.time()  # 종료시간
    print("# time : ", str(datetime.timedelta(seconds=etime - stime)), flush=True)
