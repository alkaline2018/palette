#!/usr/bin/env python
import datetime
import time
import uuid
from enum import Enum


# from env.db_conn import SpspMongoDB
from env.db_conn import ImageMongoDB
from env.db_conn_bak import Postgresql
from palette import Palette, urlOrPath
from env import db_conn_bak
import sys
import os
import shutil

from util import create_directory, get_dir_path_for_now


# NOTE: 해당 내용에선 print를 추가하면 안된다.
#  print 를 통해 다른 언어에서 사용했을 때 image_paths 를 전달하기 때문
if __name__ == "__main__":
    # 시간 체크 추후 지워도 됌
    stime = time.time()  # 시작시간

    # 경로
    AB_PATH = os.path.dirname(os.path.abspath(__file__))
    PARENT_PATH = os.path.join(AB_PATH, "../")

    # 이미지 최종 경로 반환
    image_paths = []
    # NOTE: 이미지 meta 정보 저장 DB
    #  DB는 어떤 것으로도 변경 가능하도록 만들어야 한다.
    # TODO: 설정에 따라서 1일 경우엔 mongo 2일 경우엔 postgres
    image_mongo = ImageMongoDB("mongodb")
    image_collection = image_mongo.get_collection()
    # pg = Postgresql()
    # pg.connect()
    # 외부에서 python 사용할 때 arguments 를 list로 받음 해당 내용은 url or path 로 받는다.
    _path_list = sys.argv
    # _path_list = ["","https://img1.daumcdn.net/thumb/R720x0/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fliveboard%2Fmaxmovie%2F9727ede44dd848a89ba258d2fd41fefa.JPG"]
    # 첫번째 argument 는 실행된 파이썬파일 자체라 넘기고 진행
    for v in range(1, len(_path_list)):
        down_image_path = _path_list[v]
        # path or url 을 통해 palette(이미지) 객체 생성
        palette = Palette(down_image_path)
        # get hash
        image_dict = palette.get_defalut_hash_dict()
        # hash 값으로 같은 이미지 찾기
        # TODO: 필요시 해당 내용은 postgreSQL로 변경한다.
        result = image_collection.find_one(image_dict, )
        # result = pg.find_image(image_dict)
        # 같은 이미지 있다면
        if result:
            # down_image_path 이 url 이 아니라면 해당 파일 삭제
            if not urlOrPath(down_image_path):
                os.remove(os.path.join(PARENT_PATH + down_image_path))
            # 같은 이미지의 경로를 반환
            image_paths.append(result['path'])
        # 같은 이미지 없다면
        else:
            # NOTE: 없으면 서버에서 이미지를 cp or mv해서 save -> save 후 path 받아야함
            #  cp | save 상황에 따라 다르게 적용
            #  db에 저장할 내용은 new_image_path 필요, image_hash값 c,p,d, 이미지 추출 색(속도 이슈로 제거)
            # image_dict['extractColor'] = palette.extract_color()  # 필요시 이미지 추출색 넣음 해당 내용 작성시 속도 느림
            # path 일 경우엔 이미지를 옮기고 url 일 경우엔 이미지를 생성한다. 참고
            new_image_path = ''
            new_dir_path = get_dir_path_for_now(_parent_path="public/images/", _strftime="%Y/%m/%d/%H/%M/")

            create_directory(PARENT_PATH + new_dir_path)
            # TODO: url 일때와 path 일때를 구분하여 함수화 시켜야한다.
            if urlOrPath(down_image_path):
                # url 을 바탕으로 이미지 이름 생성 png 저장 이유는 원본으로 보장된다.
                # print("url")
                # TODO: 현재 png 형태만 저장에서 image가 가지고 있는 확장자를 사용하는걸로 변경 필요
                image_name = uuid.uuid3(uuid.NAMESPACE_URL, down_image_path).__str__() + ".png"
                new_image_path = new_dir_path + image_name
                n_path = os.path.join(PARENT_PATH + new_image_path)
                # 이미지 저장
                palette.get_image().save(n_path)
            else:
                # print("path")
                # temp 이미지 경로를 image로 변경
                image_name = os.path.basename(down_image_path)
                # print("image_name: ", image_name)
                # new_image_path = down_image_path.replace("temp", "image")
                new_image_path = new_dir_path + image_name
                o_path = os.path.join(PARENT_PATH + down_image_path)
                n_path = os.path.join(PARENT_PATH + new_image_path)
                # NOTE: 필요시 copy 에서 move로 변경 할 것
                # shutil.move(o_path, n_path)
                shutil.copy(o_path, n_path)
            # NOTE: 아래 내용에서 down_image_path 대신 변경된 new_image_path 로 넣어준다.
            image_dict['path'] = new_image_path
            # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
            # pg.insert_image(image_dict)
            # con = pg.get_connect()
            # con.commit()
            _id = image_collection.insert_one(image_dict)
            image_paths.append(image_dict['path'])
    # pg.close()
    image_mongo.close()
    print(image_paths, flush=True)

