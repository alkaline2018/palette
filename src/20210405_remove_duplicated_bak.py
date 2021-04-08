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
    # TODO: original 이미지 체크 및 error 발생시 에러 내용 체크
    sp_mongo = db_conn.SpspMongoDB()

    try:
        # NOTE: 1. 몽고디비에서 thumbnailUrl or downloadPaths 중 이미지를 부른다.
        uncheck_images = sp_mongo.find_clct_images_by_check_type(_limit=10)
        results = []
        # NOTE: 2. 이미지에서 imageHash 값을 추출한다.
        for uncheck_image in uncheck_images:
            try:
                # HINT: 하나의 문서에는 여러 장의 이미지가 있을 수 있다. 이에 여러 장의 문서를 중복 처리 후
                #   해당 문서의 중복처리 결과를 반환한다.
                # TODO: 현재는 임의로 urlpath 로 잡았지만 추후 downloadPaths 로 변경한다.
                down_image_paths = [uncheck_image['thumbnailUrl']]
                ids = []
                update_dict = {}

                for down_image_path in down_image_paths:
                    palette = Palette(down_image_path)
                    image_dict = palette.get_defalut_hash_dict()
                    result = sp_mongo.find_image({"c_hash": image_dict['c_hash'], "d_hash": image_dict['d_hash'],
                                                  "p_hash": image_dict['p_hash']})
                    if result:
                        ids.append(str(result['_id']))
                    else:
                        image_dict['extract_color'] = palette.extract_color()  # 필요시 이미지 추출색 넣음 해당 내용 작성시 속도 느림
                        # TODO: 없으면 서버에서 이미지를 cp해서 save -> save 후 path 받아야함
                        #  cp | save 상황에 따라 다르게 적용
                        #  db에 저장할 내용은 new_image_path 필요, image_hash값 c,p,d, 이미지 추출 색(속도 이슈로 제거)
                        print("uncheck_image['_id']:", uncheck_image['_id'])
                        update_dict = {}
                        update_dict['duplicateCheck'] = Duplicate_check.ORIGINAL.value
                        # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
                        _id = sp_mongo.insert_image(_image_dict=image_dict)
                        ids.append(str(_id.inserted_id))
                update_dict['imageIds'] = ids
                update_dict['duplicateCheck'] = Duplicate_check.DUPLICATED.value
                result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)

                # palette = Palette(uncheck_image['thumbnailUrl'])
                # # palette = Palette("https://cr.shopping.naver.com/adcr.nhn?x=SdjjL1b3ICWfMyaoshT7G%2F%2F%2F%2Fw%3D%3DsBBeyW5RJ%2BpZRDEwdzmHYXJ4QR%2FJ9CpiJbA4CmIUSkZN7ZIoG04hikA9DI%2Fs9KTHRAao9MLVnnMHfsi%2F6jkAXL4LvkpnulXUbhzl%2FArq8TcGsKCGSMRcaby0CmGOdMAuoCDWjZ5m30BkDTbvgfAAvhLuVw3GdaDAvxDSjC3cnt2Z%2F22ms%2BW8TiQQNz%2FOHMMFFpI7ieNQiFnSyowz6LIS2Yz6Ir%2B5AOAfU8bertyJz15tlc6P1YajnJs%2FPQ4MWP%2BA7wc%2B%2FjkR2vl%2B%2B%2B%2F%2BVPNlrhRUrHESqIeqBN9PO%2B82TGOUqo4T1eSj%2F6xGLNrhtuEbaXa1PYAb0zmPF1cRoKRscXeQGFSn5i45AyoqPxx4yW3EdA4ZnT4ceB%2BlGDWLvzs522BCL3zg4U0yTs3JtBfF0%2FHZ69fkBvfSVk5i0l0lJjEbWc4nXf5tXxJGMO5e%2F2t03j%2F%2Fw7b1ceBA0Ggm7tz8tT7DokBVJz6lCEVM2%2BIyZ0mR0OWyuXo6Sx2BQiztez%2BmaP63goB6Y4br19mT6CWblxCV06IYxftTyJ%2F0LfjYPI%2BO5PcsdixOKM84nfw%2BU7IK6XVCjSPr1ISADQFG5OSwhripUqYorg60E722P2cb8d2GIDMt0AU13zuRrNlheMLDOy1Vhq%2FH77x9Zlr1IFzyuow%3D%3D&nvMid=82435583083&catId=50000821")
                # image_dict = palette.get_defalut_hash_dict()
                #
                # # NOTE: 3. 추출된 이미지 해쉬값을 통해 DB에 검색한다.
                # result = sp_mongo.find_image({"c_hash": image_dict['c_hash'], "d_hash": image_dict['d_hash'], "p_hash": image_dict['p_hash']})
                # if result:
                #     # NOTE: 있으면 해당 값을 반환한다. 필요없다면 반환하지 않아도 된다.
                #
                #     update_dict = {}
                #     update_dict['imageIds'] = result['_id']
                #
                #     update_dict['duplicate_check'] = Duplicate_check.DUPLICATED.value
                #     result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)
                #     pass
                # else:
                #     image_dict['extract_color'] = palette.extract_color() # 필요시 이미지 추출색 넣음 해당 내용 작성시 속도 느림
                #     # TODO: 없으면 서버에서 이미지를 cp해서 save -> save 후 path 받아야함
                #     #  cp | save 상황에 따라 다르게 적용
                #     #  db에 저장할 내용은 new_image_path 필요, image_hash값 c,p,d, 이미지 추출 색(속도 이슈로 제거)
                #     print("uncheck_image['_id']:", uncheck_image['_id'])
                #     update_dict = {}
                #     update_dict['duplicate_check'] = Duplicate_check.ORIGINAL.value
                #     # HINT: image collection에서 image 정보 insert 후 objectId retrun 받은 걸로 iat collection에 반영
                #     _id = sp_mongo.insert_image(_image_dict=image_dict)
                #
                #     update_dict['imageIds'] = _id.inserted_id
                #     # NOTE: 4. 반환된 값을 수집 collection에 반영한다.
                #     result = sp_mongo.update_clct_by_imageid(_query={"_id": uncheck_image['_id']}, _image_dict=update_dict)
                #     if result:
                #         results.append(result)
                #     pass

            except Exception as e:
                result = sp_mongo.update_clct_by_imageid(
                    _query={"_id": uncheck_image['_id']},
                    _image_dict={'duplicateCheck': Duplicate_check.ERROR.value}
                )
                print(f"error1: {e}")
    except Exception as e:
        print(f"error2: {e}")
    finally:
        sp_mongo.close()
    # mongo client close
    etime = time.time()  # 종료시간
    print("# 소요시간 : ", str(datetime.timedelta(seconds=etime - stime)))
