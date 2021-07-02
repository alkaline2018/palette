import unittest

from palette import PaletteUtil


class MyTestCase(unittest.TestCase):
    def test_rgb2hex(self):
        p_util = PaletteUtil()

        hex = p_util.convert_rgb2hex((53, 128, 64))
        nomal_hex = p_util.get_normaliztion_hex_by_rgb((53, 128, 64))
        self.assertEqual("#358040", hex)
        self.assertEqual("#338844", nomal_hex)

if __name__ == '__main__':
    unittest.main()
