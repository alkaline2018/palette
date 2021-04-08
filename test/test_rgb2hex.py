import unittest

from color_util import ColorUtil


class MyTestCase(unittest.TestCase):
    def test_rgb2hex(self):
        util = ColorUtil()
        hex = util.convert_rgb2hex((53, 128, 64))
        print(hex)
        print(util.get_normaliztion_hex_by_rgb((53, 128, 64)))
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
