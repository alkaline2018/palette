import requests
from PIL import Image
import imagehash
import re
from enum import Enum

from colorgram.colorgram import sample, pick_used, get_colors

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class HashType(Enum):
    """
    HINT: 이미지 해시를 만드는 방법들 입니다.
    평균 해시, 픽셀이 평균보다 크거나 같으면 각 픽셀 출력 1에 대해, 그렇지 않으면 0입니다.
    :type PERCEPTIVE_HASH: perceptive hash(인식 해시)는 평균해시(average hash)와 같은 기능을 하지만 먼저 이산 코사인 변환을 수행하고 주파수 영역에서 작동합니다.
    :type DIFFERENCE_HASH: gradient hash(경사도 or 변화도 해시), 각 픽셀의 차이를 계산하고 평균 차이와 비교합니다.
    :type COLOR_HASH: color 로 hash 값을 뽑아냄
    """
    PERCEPTIVE_HASH = 1
    DIFFERENCE_HASH = 2
    COLOR_HASH = 3

def urlOrPath(path):
    return (re.match(URL_REGEX, path) is not None)

class PaletteUtil:
    # TODO: 이미지 hash 값 비교를 통해 percent 차이 알려주기
    @staticmethod
    def diff_percent(_hash, _hash2, hash_type=HashType.PERCEPTIVE_HASH):
        """
        :type _hash: str
        :type _hash2: str
        :type hash_type: HashType
        """
        hash_size = 8
        if hash_type == HashType.COLOR_HASH:
            hash_size = 14

        __hash1 = imagehash.hex_to_flathash(_hash, hash_size)
        __hash2 = imagehash.hex_to_flathash(_hash2, hash_size)
        return __hash1.__sub__(__hash2) / hash_size ** 2

    @staticmethod
    def convert_rgb2hex(_rgb):
        """
        :type _rgb: str
        :return _hex: str
        """
        _hex = '#%02x%02x%02x' % _rgb
        return _hex

    def get_normaliztion_hex_by_rgb(self, _rgb):
        """
        :type _rgb: str
        :return normal_hex: str
        """
        _hex = self.convert_rgb2hex(_rgb)
        normal_hex = self.convert_normaliztion_by_hex(_hex)
        return normal_hex

    @staticmethod
    def convert_normaliztion_by_hex(_hex):
        """
        :type _hex: str
        :return normal_hex: str
        """
        nomal_hex = ("#" + _hex[1] + _hex[1] + _hex[3] + _hex[3] + _hex[5] + _hex[5])
        return nomal_hex


class Palette:
    HASH_SIZE = 8
    COLOR_HASH_SIZE = 3
    DETAIL_HASH_SIZE = 10

    def __init__(self, url_or_path=None):
        """
        :type url_or_path: str
        """
        if(url_or_path is None):
            print("None")
        elif(type(url_or_path) != str):
            print("path != str")
            raise TypeError
        elif urlOrPath(url_or_path):
            # print("url")
            self.image = Image.open(requests.get(url_or_path, stream=True).raw)
        else:
            # print("path")
            self.image = Image.open(url_or_path)
        self.defalut_hash_dict = {
            "p_hash": self.make_hash(HashType.PERCEPTIVE_HASH, self.HASH_SIZE).__str__(),
            "d_hash": self.make_hash(HashType.DIFFERENCE_HASH, self.HASH_SIZE).__str__(),
            "c_hash": self.make_hash(HashType.COLOR_HASH, self.COLOR_HASH_SIZE).__str__(),
            "pdc_detail_hash": self.make_hash(HashType.PERCEPTIVE_HASH, self.DETAIL_HASH_SIZE).__str__()+"_"+self.make_hash(HashType.DIFFERENCE_HASH, self.DETAIL_HASH_SIZE).__str__()+"_"+self.make_hash(HashType.COLOR_HASH, self.DETAIL_HASH_SIZE).__str__(),
        }

    # TODO: 같은 이미지인지 확인 -> DB로 p,d,c hash eq 확인
    def __eq__(self, other):
        """
        :type other: Palette
        :return boolean
        """
        return self.defalut_hash_dict == other.defalut_hash_dict

    def __ne__(self, other):
        """
        :type other: Palette
        :return boolean
        """
        return self.defalut_hash_dict != other.defalut_hash_dict

    def get_defalut_hash_dict(self):
        return self.defalut_hash_dict

    def get_image(self):
        return self.image

    def make_hash(self, hash_type: HashType, hash_size: int):
        """
        :type hash_type: HashType
        :type hash_size: int
        :return image_hash
        """
        if hash_type == HashType.PERCEPTIVE_HASH:
            image_hash = imagehash.phash(self.image, hash_size)
        elif hash_type == HashType.DIFFERENCE_HASH:
            image_hash = imagehash.dhash(self.image, hash_size)
        elif hash_type == HashType.COLOR_HASH:
            image_hash = imagehash.colorhash(self.image, hash_size)
        return image_hash

    def extract_color(self, number_of_colors=6):
        """
        최대 256개
        :type number_of_colors: int
        """
        _image = self.image.convert('RGB')

        samples = sample(_image)
        used = pick_used(samples)
        used.sort(key=lambda x: x[0], reverse=True)
        c_list = []
        p_util = PaletteUtil()
        for _color in get_colors(samples, used, number_of_colors):
            c_list.append(
                {"rgb": {"r": _color.rgb.r, "g": _color.rgb.g, "b": _color.rgb.b},
                 "proportion": _color.proportion,
                 "hex": p_util.convert_rgb2hex((_color.rgb.r, _color.rgb.g, _color.rgb.b))}
            )
        return c_list
