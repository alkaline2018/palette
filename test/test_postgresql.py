import unittest

from env.db_conn import Postgresql


class MyTestCase(unittest.TestCase):


    def test_find_image(self):
        pg = Postgresql()
        pg.connect()
        result = pg.find_image({'p_hash': 'ab91442f77c2c96c', 'd_hash': 'f0a793d90f63a322', 'c_hash': '07006000000', 'pdc_detail_hash': 'ab647440bd7734bc9db0327c8_f83c6daf634ec9a39cc3b0e86_033ff1f800003ff00000078000000000000'})
        print(result)
        pg.close()

    def test_select(self):
        pg = Postgresql()
        pg.connect()
        results = pg.find_all_image()
        pg.close()
        print(results)

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
