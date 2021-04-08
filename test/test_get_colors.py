import os
import unittest

from PIL import Image

from color_util import ColorUtil
import extcolors
import colorgram
import array

class MyTestCase(unittest.TestCase):

    def test_conver_image(self):
        # IMAGE_SIZE = (50, 50)
        # 1
        # L
        # RGB
        # RGBX

        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        im = Image.open(CONFIG_PATH + "/../static/image/cafe.jpg").convert("RGB").convert("L").convert("1")
        # url = "https://imgnews.pstatic.net/image/029/2021/03/12/0002660482_001_20210312070406814.jpg?type=w647"
        # im = Image.open(requests.get(url, stream=True).raw).convert("RGB")
        # im = im.resize(IMAGE_SIZE, Image.LANCZOS)
        im.save("../static/result/cafe_resize.jpg")

    def test_shift(self):
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        file_path = CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png"
        image = Image.open(file_path)
        top_two_bits = 0b11000000
        ARRAY_DATATYPE = 'l'
        sides = 1 << 2  # Left by the number of bits used.
        cubes = sides ** 7
        print(sides)
        print(cubes)
        samples = array.array(ARRAY_DATATYPE, (0 for _ in range(cubes)))
        # print(samples)
        width, height = image.size
        pixels = image.load()
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]
                Y = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
                packed = (Y & top_two_bits) << 4
                print(packed)


    def test_colorgram(self):
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        file_path = CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png"
        colors = colorgram.extract(file_path, 6)
        print(colors)

    def test_ext_colors(self):
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        colors, pixel_count = extcolors.extract_from_path(CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png")
        print(colors)


    def test_get_colors(self):
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))

        im = Image.open(CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png").convert("P", palette=Image.ADAPTIVE, colors=30).convert("RGB")
        # pixels = list(im.getdata())
        # print(pixels)
        util = ColorUtil()
        # print(im.getcolors())

        color_dict_list = [{"count": i[0],"color": util.get_normaliztion_hex_by_rgb(i[1])} for i in im.getcolors()]
        # print(color_dict_list)
        color_dict_list_sorted = sorted(color_dict_list, key=lambda color_dict: (color_dict["color"]), reverse=True)
        print(color_dict_list_sorted)
        _list = []

        for i in range(1, len(color_dict_list_sorted)):
            if (color_dict_list_sorted[i-1]['color'] == color_dict_list_sorted[i]['color']):
                color_dict_list_sorted[i]['count'] = color_dict_list_sorted[i-1]['count'] + color_dict_list_sorted[i]['count']
            else:
                _list.append(color_dict_list_sorted[i-1])
            if i == len(color_dict_list_sorted)-1:
                _list.append(color_dict_list_sorted[i])
        _list = sorted(_list, key=lambda color_dict: (color_dict["count"]), reverse=True)
        print(_list)
        print(len(_list))
            # color_dict_list_sorted[i] = color_dict_list_sorted[i]



        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
