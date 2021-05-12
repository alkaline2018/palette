import unittest
from datetime import datetime

from util import create_directory


class MyTestCase(unittest.TestCase):
    def test_datetime(self):
        now = datetime.now()
        nowDate = now.strftime('%Y%m%d%H%M%S')
        print(nowDate)  # 2018-07-28

    def test_create_directory(self):
        now_date = datetime.now()
        now_dir_structure = now_date.strftime("%Y/%m/%d/%H/%M")
        create_directory("../public/images/"+now_dir_structure)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
