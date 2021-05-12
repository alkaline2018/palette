from enum import Enum


# NOTE: 각 문서마다 가지고 있는 상태
class Duplicate_check(Enum):
    """
    HINT:
    :type NO_IMAGE: 이미지가 없다.
    :type NO_DOWNLOAD_IMAGE: 모든 다운로드 작업이 시작되지 않았다.
    :type PART_DOWNLOAD_IMAGE: 일부 다운로드 작업이 시작됐다.
    :type ALL_DOWNLOAD_IMAGE: 모든 이미지가 다운로드 작업이 완료되었다.
    :type DUPLICATED: 오리지날 이미지에서 파생된 중복이미지
    :type ERROR: 원인을 알 수 없는 나머지 ERROR
    # :type FILE_NOT_FOUND_ERROR: FILE 없어서 발생한 ERROR
    # :type IMAGE_INSERT_ERROR: 이미지 INSERT 중 발생한 ERROR
    # :type IMAGE_SAVE_ERROR: 이미지 저장중 발생한 ERROR
    """
    NO_IMAGE = 0
    NO_DOWNLOAD_IMAGE = 1
    PART_DOWNLOAD_IMAGE = 2
    ALL_DOWNLOAD_IMAGE = 3
    DUPLICATED = 4
    ERROR = 5
    # FILE_NOT_FOUND_ERROR = 6
    # IMAGE_INSERT_ERROR = 5
    # IMAGE_SAVE_ERROR = 6


# NOTE: 각 이미지마다 가지고 있는 상태
class Image_status(Enum):
    """
    HINT:
    :type BEFORE_DOWNLOAD: 이미지 다운로드 전
    :type AFTER_DOWNLOAD: 이미지 다운로드 후
    :type ERROR_DOWNLOAD: 이미지 다운로드 중 ERROR 발생
    :type DUPLICATED: 이미지 중복검사 완료
    :type ERROR_DUPLICATED: 이미지 중복검사 중 ERROR 발생
    :type FILE_NOT_FOUND_ERROR_DUPLICATED: 이미지 중복검사 중 FILE_NOT_FOUND_ERROR 발생
    """
    BEFORE_DOWNLOAD = 1
    AFTER_DOWNLOAD = 2
    ERROR_DOWNLOAD = 3
    DUPLICATED = 4
    ERROR_DUPLICATED = 5
    FILE_NOT_FOUND_ERROR_DUPLICATED = 6
