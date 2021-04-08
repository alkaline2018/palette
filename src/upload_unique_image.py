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
    # 시간 체크 추후 지워도 됌
    stime = time.time()  # 시작시간
    # 이미지 최종 경로 반환
    results = []
    # NOTE: 이미지 meta 정보 저장 DB
    #  DB는 어떤 것으로도 변경 가능하도록 만들어야 한다.
    sp_mongo = db_conn.SpspMongoDB()
    # 외부에서 python 사용할 때 arguments 를 list로 받음 해당 내용은 url or path 로 받는다.
    _path_list = sys.argv
    # _path_list = ["","https://img2.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202104/08/chosun/20210408080322607oofo.jpg"]
    # 첫번째 argument 는 실행된 파이썬파일 자체라 넘기고 진행
    for v in range(1, len(_path_list)):
        down_image_path = _path_list[v]
        # path or url 을 통해 palette(이미지) 객체 생성
        palette = Palette(down_image_path)
        # get hash
        image_dict = palette.get_defalut_hash_dict()
        # hash 값으로 같은 이미지 찾기
        result = sp_mongo.find_image(image_dict)
        # 현재 파일의 절대경로
        ab_path = os.path.dirname(os.path.abspath(__file__))
        # 같은 이미지 있다면
        if result:
            # down_image_path 이 url 이 아니라면 해당 파일 삭제
            if not urlOrPath(down_image_path):
                os.remove(os.path.join(ab_path, "../" + down_image_path))
            # 해당 결과는 수집 collection 에 반영
            results.append(result['path'])
        # 같은 이미지 없다면
        else:
            # NOTE: 없으면 서버에서 이미지를 cp or mv해서 save -> save 후 path 받아야함
            #  cp | save 상황에 따라 다르게 적용
            #  db에 저장할 내용은 new_image_path 필요, image_hash값 c,p,d, 이미지 추출 색(속도 이슈로 제거)
            # image_dict['extractColor'] = palette.extract_color()  # 필요시 이미지 추출색 넣음 해당 내용 작성시 속도 느림
            # path 일 경우엔 이미지를 옮기고 url 일 경우엔 이미지를 생성한다. 참고
            new_image_path = ''
            if urlOrPath(down_image_path):
                # url 을 바탕으로 이미지 이름 생성 jpg 저장 이유는 손실저장 방식이라 용량이 절감된다.
                # print("url")
                new_image_path = "public/image/"+uuid.uuid3(uuid.NAMESPACE_URL, down_image_path).__str__()+".jpg"
                n_path = os.path.join(ab_path, "../" + new_image_path)
                # 이미지 저장
                palette.get_image().save(n_path)
            else:
                # print("path")
                # temp 이미지 경로를 image로 변경
                new_image_path = down_image_path.replace("temp", "image")
                o_path = os.path.join(ab_path, "../"+down_image_path)
                n_path = os.path.join(ab_path, "../"+new_image_path)
                shutil.move(o_path, n_path)
            # NOTE: 아래 내용에서 down_image_path 대신 변경된 new_image_path 로 넣어준다.
            image_dict['path'] = new_image_path
            # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
            _id = sp_mongo.insert_image(_image_dict=image_dict)
            results.append(image_dict['path'])
    print(results, flush=True)

