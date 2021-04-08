import unittest

from PIL import Image

from palette import Palette, HashType, PaletteUtil, urlOrPath
import os

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        file_name = "cafe.jpg"
        self.image_path = (CONFIG_PATH + "/../static/image/" + file_name)
        file_name2 = "cafe_4.jpg"
        self.image_path2 = (CONFIG_PATH + "/../static/image/" + file_name2)
        self.image_url = "https://imgnews.pstatic.net/image/029/2021/03/12/0002660482_001_20210312070406814.jpg?type=w647"

    def test_init_url(self):
        palette = Palette(self.image_url)
        print("DIFFERENCE_HASH:", palette.make_hash(HashType.DIFFERENCE_HASH, 8).__str__())
        self.assertEqual("f0e4ecd8f5656060", palette.make_hash(HashType.DIFFERENCE_HASH, 8).__str__())

    def test_init_path(self):
        palette = Palette(self.image_path)
        print(palette.get_image())

    def test_eq(self):
        palette2 = Palette(self.image_path)
        palette3 = Palette(self.image_path2)
        self.assertTrue(palette2.__eq__(palette3))

    def test_ne(self):
        palette = Palette(self.image_url)
        palette2 = Palette(self.image_path)
        self.assertTrue(palette.__ne__(palette2))

    def test_extract_color(self):
        palette = Palette(self.image_path)
        print(palette.extract_color())

    def test_image_save(self):
        palette = Palette(self.image_url)
        if urlOrPath(self.image_url):
            print("url")
            _im = palette.get_image()
            _im.save("./test2.jpg")
        else:
            print("path")


    def test_diff_percent(self):
        palette = Palette(self.image_path)
        d_hash1 = palette.make_hash(HashType.DIFFERENCE_HASH, 8).__str__()
        palette2 = Palette(self.image_path2)
        d_hash2 = palette2.make_hash(HashType.DIFFERENCE_HASH, 8).__str__()
        print(PaletteUtil().diff_percent(d_hash1, d_hash2))
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
