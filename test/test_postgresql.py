import unittest

from env.db_conn import Postgresql


class MyTestCase(unittest.TestCase):

    def test_insert_image(self):
        image_dict = {'p_hash': '8d31d621c75c9be2', 'd_hash': '6abe3174cab33444', 'c_hash': '061c0000000',
         'pdc_detail_hash': '8dec5d6885c79729b78ad8892_74ad6195e579154d8aea635ad_0fbfe1f3fd01c7c000010183e0000300000',
         'path': 'public/image/2021/04/12/17/24/7fa6209f-13a7-343f-bad2-8e4f81f98a96.png'}
        pg = Postgresql()
        pg.connect()
        pg.insert_image(image_dict)
        con =pg.get_connect()
        con.commit()
        pg.close()


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
