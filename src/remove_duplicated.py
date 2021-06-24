import datetime
import time
from enum import Enum

from env import db_conn
# from env.db_conn import SpspMongoDB
from palette import Palette


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
    sp_mongo = db_conn.SpspMongoDB()

    try:
        # NOTE: 1. 몽고디비에서 thumbnailUrl or downloadPaths 중 이미지를 부른다.
        uncheck_images = sp_mongo.find_clct_images_by_check_type(_limit=5)
        # results = []
        # NOTE: 2. 이미지에서 imageHash 값을 추출한다.
        for uncheck_image in uncheck_images:
            try:
                # HINT: 하나의 문서에는 여러 장의 이미지가 있을 수 있다. 이에 여러 장의 이미지를 중복 처리한다.
                # TODO: 현재는 임의로 urlpath 로 잡았지만 추후 downloadPaths 로 변경한다.
                down_image_paths = [uncheck_image['thumbnailUrl'], uncheck_image['thumbnailUrl']]
                ids = []
                update_dict = {}

                for down_image_path in down_image_paths:
                    # new 이미지
                    palette = Palette(down_image_path)
                    # get hash
                    image_dict = palette.get_defalut_hash_dict()
                    result = sp_mongo.find_image({"c_hash": image_dict['c_hash'], "d_hash": image_dict['d_hash'],
                                                  "p_hash": image_dict['p_hash']})
                    if result:
                        # 해당 결과는 수집 collection 에 반영
                        ids.append(result['_id'])
                    else:
                        # NOTE: extractColor 는 속도 이슈로 현재는 사용하지 않는다. 추가로 필요했을 경우 따로 만들어서 넣어주자.
                        # image_dict['extractColor'] = palette.extract_color()  # 필요시 이미지 추출색 넣음 해당 내용 작성시 속도 느림
                        # TODO: 없으면 서버에서 이미지를 cp해서 save -> save 후 path 받아야함
                        #  cp | save 상황에 따라 다르게 적용
                        #  db에 저장할 내용은 new_image_path 필요, image_hash값 c,p,d, 이미지 추출 색(속도 이슈로 제거)
                        # print("uncheck_image['_id']:", uncheck_image['_id'])
                        # TODO: 아래 내용에서 down_image_path 대신 변경된 unique_image_path 로 넣어준다.
                        unique_image_path = down_image_path
                        image_dict['path'] = unique_image_path
                        # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
                        _id = sp_mongo.insert_by_dict(_dict=image_dict)
                        ids.append(_id.inserted_id)

                update_dict['imageIds'] = ids
                update_dict['duplicateCheck'] = Duplicate_check.DUPLICATED.value
                result = sp_mongo.update_one_by_query(_query={"_id": uncheck_image['_id']}, _dict=update_dict)

            except Exception as e:
                result = sp_mongo.update_one_by_query(
                    _query={"_id": uncheck_image['_id']},
                    _dict={'duplicateCheck': Duplicate_check.ERROR.value}
                )
                print(f"error1: {e}", flush=True)
    except Exception as e:
        print(f"error2: {e}", flush=True)
    finally:
        sp_mongo.close()
    # mongo client close
    etime = time.time()  # 종료시간
    print("# 소요시간 : ", str(datetime.timedelta(seconds=etime - stime)), flush=True)
