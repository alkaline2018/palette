#!/usr/bin/env python
import datetime
import re
import time
import uuid



# from env.db_conn import SpspMongoDB
from imageEnums import Duplicate_check, Image_status
from palette import Palette, urlOrPath
from env import db_conn
import sys
import os
import shutil
from datetime import datetime, timedelta
from PIL import ImageFilter
from PIL import ImageEnhance

from util import convert_image_insert

if __name__ == "__main__":
    stime = time.time()  # 시작시간
    results = []
    sp_mongo = db_conn.SpspMongoDB()
    sp_db = sp_mongo.db

    # collection을 각기 분리되어있다.

    try:
        # NOTE: 1. 몽고디비에서 이미지를 부른다.
        # TODO: image_[channel]_[날짜] 를 불러 이를 find 한다. 반복문을 통해 전체를 부른다.
        #   collection 은 parameter로 변경되어 작동할 것
        collection_names = sp_db.list_collection_names()
        for collection_name in collection_names:
            # re.findall("^test_image(.+)202105\d{2}", str(collection_name))
            if re.findall("^test_image(.+)202105\d{2}", str(collection_name)):
                uncheck_images = sp_mongo.find_clct_images_by_check_type(_collection=sp_db[str(collection_name)], _limit=10)
                # results = []
                # NOTE: 2. 이미지에서 imageHash 값을 추출한다.
                for uncheck_image in uncheck_images:
                    try:
                        # HINT: 하나의 문서에는 여러 장의 이미지가 있을 수 있다. 이에 여러 장의 이미지를 중복 처리한다.
                        # TODO: 현재는 임의로 thumbnailUrl 로 잡았지만 추후 downloadPaths 로 변경한다.
                        down_images = uncheck_image['images']
                        down_image_channel = uncheck_image['channel']
                        update_dict = {}
                        document_images = []

                        ab_path = os.path.dirname(os.path.abspath(__file__))
                        for down_image in down_images:
                            # todo: if urlOrPath(down_image_path):
                            down_image_path = down_image['path']
                            if not urlOrPath(down_image_path):
                                down_image_path = os.path.join(ab_path, "../public/source", down_image_channel, "." + down_image_path)

                            # new 이미지
                            # TODO: o_path = public/source/down_image_channel/down_image_path 로 집어 넣을 것
                            #   down_image_path url인지 아닌지 판단해야한다.

                            # NOTE: path 에 파일이 없으면 에러 발생
                            try:
                                palette = Palette(down_image_path)
                                # get hash
                                image_dict = palette.get_defalut_hash_dict().copy()
                                result = sp_mongo.find_image(image_dict)
                                if result:
                                    down_image['id'] = result['_id']
                                    down_image['status'] = Image_status.DUPLICATED.value
                                    # todo: images 각 이미지 status 상태 변경
                                    document_images.append(down_image)
                                    # todo: 추후 삭제
                                    # 해당 결과는 수집 collection 에 반영
                                    # ids.append(result['_id'])
                                else:
                                    new_image_path = ''
                                    if urlOrPath(down_image_path):
                                        # HINT: url 을 바탕으로 이미지 이름 생성 jpg 저장 이유는 손실저장 방식이라 용량이 절감된다.
                                        #   만약 원본 이미지에 가깝게 저장하고 싶다면 png로 저장 다만 저장 방식 때문에 용량이 크게 늘어날 수 있다.
                                        # print("url")

                                        new_image_path = "public/images/" + uuid.uuid3(uuid.NAMESPACE_URL,
                                                                                       down_image_path).__str__() + ".jpg"
                                        n_path = os.path.join(ab_path, "../" + new_image_path)

                                        # 이미지 저장
                                        palette.get_image().save(n_path)
                                    else:
                                        # 이미지 복사는 이미지 상태가 저장 후 일 경우에만 작동한다.
                                        if down_image['status'] == Image_status.AFTER_DOWNLOAD.value:
                                            # TODO: 이미지 경로가 바뀌었으면 새롭게 저장하는 법도 바뀌어야 한다.
                                            # print("path")
                                            # temp 이미지 경로를 image로 변경
                                            # TODO:
                                            #  o_path = public/source/down_image_channel/down_image_path
                                            #  n_path = public/images/down_image_path

                                            # new_image_path = down_image_path.replace("temp", "images")
                                            # o_path = os.path.join(ab_path, "../" + down_image_path)
                                            n_path = os.path.join(ab_path, "../public/images", "." + down_image['path'])
                                            n_dir = os.path.dirname(n_path)

                                            if not os.path.exists(n_dir):
                                                os.makedirs(n_dir)
                                            # NOTE: 필요시 copy 에서 move로 변경 할 것
                                            # shutil.move(o_path, n_path)
                                            shutil.copy(down_image_path, n_path)
                                            # TODO: 신규 test 이미지 생성 및 해당 내용
                                            print(n_path)
                                    # NOTE: 아래 내용에서 down_image_path 대신 변경된 new_image_path 로 넣어준다.
                                    # image_dict['path'] = new_image_path
                                    image_dict['path'] = down_image['path']
                                    image_dict["collectDatetime"] = datetime.now().strftime('%Y%m%d%H%M%S')
                                    # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
                                    _id = sp_mongo.insert_image(_image_dict=image_dict)

                                    # NOTE: image 를 convert 시켜 save 하고 DB에 insert 한다 현재 4개의 이미지가 생성된다.
                                    convert_image_insert(palette, n_path, down_image['path'], _id.inserted_id, sp_mongo)

                                    down_image['id'] = _id.inserted_id
                                    down_image['status'] = Image_status.DUPLICATED.value
                                    # todo: images 각 이미지 status 상태 변경
                                    document_images.append(down_image)
                            except FileNotFoundError as e:
                                down_image['status'] = Image_status.FILE_NOT_FOUND_ERROR.value
                                document_images.append(down_image)
                                update_dict['imagesStatus'] = Duplicate_check.ERROR.value
                                print(f"[{uncheck_image['_id']}]error_file_not_found early: {e}", flush=True)
                            except Exception as e:
                                down_image['status'] = Image_status.ERROR_DUPLICATED.value
                                document_images.append(down_image)
                                update_dict['imagesStatus'] = Duplicate_check.ERROR.value
                                print(f"[{uncheck_image['_id']}]error early: {e}", flush=True)

                        # update_dict['imageIds'] = ids
                        update_dict['images'] = document_images
                        if 'imagesStatus' not in update_dict.keys():
                            update_dict['imagesStatus'] = Duplicate_check.DUPLICATED.value
                        # result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)

                    except Exception as e:
                        update_dict['imagesStatus'] = Duplicate_check.ERROR.value
                        print(f"[{uncheck_image['_id']}]error1: {e}", flush=True)
                    finally:
                        result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)
    except Exception as e:
        print(f"error2: {e}", flush=True)
    finally:
        sp_mongo.close()
    # mongo client close
    etime = time.time()  # 종료시간
    print("# time : ", str(timedelta(seconds=etime - stime)), flush=True)

